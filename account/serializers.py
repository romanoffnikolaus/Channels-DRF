from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.mail import send_mail

from .tasks import send_activation_code_celery
from announcement.models import Announcement
from announcement.serializers import AnnouncementSerializer

User = get_user_model()


class Profileserializer(serializers.ModelSerializer):
    users_announsments = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_users_announsments(self, instance):
        programs = instance.announcements.filter(user=instance).prefetch_related('announcementImages')
        program_serializer = AnnouncementSerializer(programs, many=True)
        return program_serializer.data


class Registrationserializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(required=True, write_only=True)
    id = serializers.ReadOnlyField()
    date_joined = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
            'password_confirm',
            'first_name',
            'last_name',
            'date_joined',
            'telegram_url',
            'about_user',
            'phone_number',
        ]

    def validate(self, attrs):
        confirm = attrs.pop('password_confirm')
        password = attrs['password']
        if password != confirm:
            raise serializers.ValidationError(
                'Пароли не совпадают'
            )
        return super().validate(attrs)
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        send_activation_code_celery(user.email, user.activation_code)
        user.save()
        return user
    
    def validate_telegram_url(self, telegram_url):
        if not telegram_url.startswith('https://t.me/'):
            raise serializers.ValidationError('Uncorrect telegram link. Example: "https://t.me/Username"')
        return telegram_url
    
    def validate_phone_number(self, phone_number: str):
        if not phone_number.startswith('+996') or phone_number.startswith('+7') and phone_number[1:].isnumeric():
            raise serializers.ValidationError('Uncorrect format for phone number. Example: +74952222222 or +996700400400')
        return phone_number
    

class ChangePasswordSerializer(serializers.ModelSerializer):
    
    old_password = serializers.CharField(
        min_length=4, required=True
    )
    new_password = serializers.CharField(
        min_length=4, required=True
    )
    new_password_confirm = serializers.CharField(
        min_length=4, required=True
    )

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'new_password_confirm')

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        new_password_confirm = attrs.pop('new_password_confirm')
        if new_password != new_password_confirm:
            raise serializers.ValidationError('Password mismatch!')
        return attrs

    def validate_old_password(self, old_password):
        user = self.context['request'].user
        if not user.check_password(old_password):
            raise serializers.ValidationError('Uncorrecct password')
        return old_password

    def set_new_password(self):
        user = self.context['request'].user
        new_password = self.validated_data.get('new_password')
        user.set_password(new_password)
        user.save()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User is not found")
        return email

    def send_verification_email(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_mail(
            'Password recovery',
            f'Your activation code: {user.activation_code}',
            'example@gmail.com',
            [user.email]
        )


class ForgotPasswordCompleteSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=4, required=True)
    password_confirm = serializers.CharField(min_length=4, required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        password1 = attrs.get('password')
        password2 = attrs.get('password_confirm')
        if not User.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError('User is not found or wrong activation code')
        if password1 != password2:
            raise serializers.ValidationError('Password mismatch!')
        return attrs

    def set_new_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.activation_code = ''
        user.save()

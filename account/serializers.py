from django.contrib.auth import get_user_model
from rest_framework import serializers
from .tasks import send_activation_code_celery


User = get_user_model()

class Profileserializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


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
    class Meta:
        model = User
        fields = '__all__'


class ForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

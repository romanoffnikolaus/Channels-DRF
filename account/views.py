from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from . import serializers


User = get_user_model()

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.Profileserializer

    @swagger_auto_schema(tags=['account'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['account'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(request_body=serializers.Registrationserializer, tags=['account'])    
    def create(self, request, *args, **kwargs):
        self.serializer_class = serializers.Registrationserializer
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(request_body=serializer_class, tags=['account'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(request_body=serializer_class, tags=['account'])    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(request_body=serializers.ChangePasswordSerializer, tags=['account'])
    @action(detail=False, methods=['POST'])
    def change_password(self, request, *args, **kwargs):
        pass

    @swagger_auto_schema(request_body=serializers.ForgotPasswordSerializer, tags=['account'])
    @action(detail=False, methods=['POST'])
    def forgot_password(self, request, *args, **kwargs):
        serializer = serializers.ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_verification_email()
            return Response('You will receive a link to reset your password.')

    @swagger_auto_schema(request_body=serializers.ForgotPasswordCompleteSerializer, tags=['account'])
    @action(detail=False, methods=['POST'])
    def forgot_password_complete(self, request, *args, **kwargs):
        serializer = serializers.ChangePasswordSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            message = 'Successful'
            return Response(serializer.validated_data)
        else:
            message = 'Uncorrecct password'
            return Response(message)
        
class ActivationView(APIView):
    def get(self, request, email, activation_code):
        user = User.objects.filter(
            email=email,
            activation_code=activation_code).first()
        if not user:
            return Response('User is not found', status=400)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response('Activated', status=200)






from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from slugify import slugify
from django.utils.crypto import get_random_string


class UserManager(BaseUserManager):
    """Менеджер для создания разных типов юзеров"""
    
    def _create(self, email, password, **kwargs):
        self.email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.create_activation_code()
        user.save()
        return user
    
    def create_user(self, email, password, **kwargs):
        return self._create(email, password, **kwargs)
    
    def create_superuser(self, email, password, **kwargs):
        user = self._create(email, password, **kwargs)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()


class User(AbstractUser):
    """Дополненный класс AbstractUser"""

    objects = UserManager()
    username = ''
    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now=True)
    telegram_url = models.URLField(max_length=255, blank=True)
    about_user = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='profile/', blank=True)
    
    
    activation_code =models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        indexes = [models.Index(fields=['email']),]

    def __str__(self) -> str:
        return self.email
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.first_name)
        return super().save(*args, **kwargs)
    
    def create_activation_code(self):
        """Создает код активации из 10 символов для пользователя"""

        allowed_chars='qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
        self.activation_code = get_random_string(length=10, allowed_chars=allowed_chars)
        self.save()
        

class UserPhotos(models.Model):
    image = models.ImageField(upload_to='userImages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userPhotos')

    def __str__(self) -> str:
        return self.user, self.pk



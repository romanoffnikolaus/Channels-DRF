from .utils import send_activation_code
from django.core.mail import send_mail
from core.celery_conf import app
from django.contrib.auth import get_user_model


User = get_user_model()


@app.task
def send_activation_code_celery(email, activation_code):
    send_activation_code(email, activation_code)


@app.task
def send_notification_email(email):
    message = 'Вы отправили адрес для добавления его в каталог на нашем сайте. Свяжитесь с администрацией для подтверждения адреса.'
    send_mail(
        'Внесение адреса в каталог',
        message,
        'romanoffnikolaus@gmail.com',
        [email],
        fail_silently=False
    )
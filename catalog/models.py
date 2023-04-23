from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()



class Catalog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='catalog')
    adress = models.CharField(blank=False, max_length=255)
    choices_type = (('hostel', 'Хостел/Приют'),('clinic','Ветклиника'),('zooshop','Зоомагазин'), ('babysitter', 'Зооняни'))
    adress_type = models.CharField(blank=False, max_length=50, choices=choices_type)
    verified_adress = models.BooleanField(default=False)
    title = models.CharField(blank=False, max_length=150)
    image = models.ImageField(upload_to='catalogImages')
    phone_number = models.CharField(blank=False, max_length=20)
    loc_choices = (('Бишкек', 'Бишкек'), ('Ош', 'Ош'), ('Нарын', 'Нарын'), ('Иссык-куль','Иссык-куль'), ('Баткен', 'Баткен'), ('Талас','Талас'), ('Джалал-Абад','Джалал-Абад'))
    location = models.CharField(blank=False, max_length=20, choices=loc_choices)

    def __str__(self) -> str:
        return self.adress
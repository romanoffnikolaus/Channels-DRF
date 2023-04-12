from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()



class Catalog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='catalog')
    adress = models.CharField(blank=False, max_length=100)
    choices_type = (('hostel', 'Хостел/Приют'),('clinic','Ветклиника'),('zooshop','Зоомагазин'))
    adress_type = models.CharField(blank=False, max_length=50, choices=choices_type)
    verified_adress = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.adress
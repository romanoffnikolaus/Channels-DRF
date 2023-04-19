from django.db import models
from account.models import User

class Room(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_rooms')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_rooms')


class Message(models.Model):
    date = models.DateTimeField(auto_now_add=True, )
    content = models.TextField(blank=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_messges')






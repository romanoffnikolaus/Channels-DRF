from django.db import models
from account.models import User

class Room(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_rooms')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_rooms')

    def __str__(self) -> str:
        return f'{self.customer.id} | {self.seller.id}'


class Message(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_messages')
    # author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='w

    @property
    def publishdate(self):
        return self.date.strftime('%Y-%m-%d:%H:%M')
    
    def __str__(self) -> str:
        return f'{self.room}'







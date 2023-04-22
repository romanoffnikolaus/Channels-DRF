from django.db import models
from account.models import User
from announcement.models import Announcement


class Room(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_rooms')
    announcement = models.ForeignKey(Announcement, models.CASCADE, related_name='rooms')

    def __str__(self) -> str:
        return f'{self.customer.id} | {self.announcement} | {self.announcement.user.id}'

    
class Message(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_messages')

    @property
    def publishdate(self):
        return self.date.strftime('%Y-%m-%d:%H:%M')
    
    def __str__(self) -> str:
        return f'{self.room}'







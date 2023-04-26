from django.db import models
from django.contrib.auth import get_user_model

from announcement.models import Announcement
from announcement.models import Announcement

User = get_user_model()


class Like(models.Model):
    pass

class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites')
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    is_favorite = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.announcement.title} in favorites of user: {self.user.id}'
    

class UserComment(models.Model):
    pass

class AnnouncementComment(models.Model):
    announsment = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    comment = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} comment on: {self.announsment}'
    

class ForumPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_forum_posts')
    body = models.TextField(max_length=255)

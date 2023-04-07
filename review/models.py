from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Like(models.Model):
    pass

class Favorite(models.Model):
    pass

class UserComment(models.Model):
    pass

class AnnouncementComment(models.Model):
    pass
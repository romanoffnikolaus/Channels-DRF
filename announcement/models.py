from django.db import models
from django.contrib.auth import get_user_model
from slugify import slugify

User = get_user_model()

class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=100, blank=False)
    price = models.DecimalField(blank=True)
    slug = models.SlugField(blank=False)

    def __str__(self) -> str:
        return self.title

    def save(self, *agrs, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*agrs, **kwargs)


class AnnouncementPhoto(models.Model):
    image = models.ImageField(upload_to='announcementImages')
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='announcementImages')

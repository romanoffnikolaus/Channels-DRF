from django.db import models
from django.contrib.auth import get_user_model
from slugify import slugify

User = get_user_model()

class Announcement(models.Model):

    class Meta:
        verbose_name_plural = 'Announcements'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=100, blank=False)
    price = models.DecimalField(blank=True, max_digits=6, decimal_places=2)
    slug = models.SlugField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *agrs, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*agrs, **kwargs)


class AnnouncementPhoto(models.Model):
    image = models.ImageField(upload_to='announcementImages')
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='announcementImages')

from django.db import models
from django.contrib.auth import get_user_model
from slugify import slugify
from datetime import datetime, timedelta
from django.db.models.functions import TruncMonth

from categories.models import Category

User = get_user_model()

class Announcement(models.Model):
    """Модель для создания объявлений"""

    class Meta:
        verbose_name_plural = 'Announcements'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=100, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='announcements')
    price = models.DecimalField(blank=True, null = True, max_digits=6, decimal_places=2)
    slug = models.SlugField(blank=True, primary_key=True)
    description = models.CharField(blank=False, max_length=255)
    loc_choices = (('Бишкек', 'Бишкек'), ('Ош', 'Ош'), ('Нарын', 'Нарын'), ('Иссык-куль','Иссык-куль'), ('Баткен', 'Баткен'), ('Талас','Талас'), ('Джалал-Абад','Джалал-Абад'))
    location = models.CharField(blank=False, max_length=20, choices=loc_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.PositiveBigIntegerField(default=0)
    phone_number = models.CharField(max_length=20, blank=False)

    def __str__(self) -> str:
        return self.title

    def save(self, *agrs, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*agrs, **kwargs)

    def get_today_count(self):
        today = datetime.now().date()
        return Announcement.objects.filter(created_at__date=today).count()

    def get_month_count(self):
        month_ago = datetime.now().date() - timedelta(days=30)
        return Announcement.objects.filter(created_at__date__gte=month_ago).count()

    get_today_count.short_description = 'Today Count'
    get_month_count.short_description = 'Month Count'


class AnnouncementPhoto(models.Model):
    image = models.ImageField(upload_to='announcementImages/')
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='announcementImages')

    class Meta:
        indexes = [models.Index(fields=['announcement']),]

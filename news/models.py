from django.db import models
from slugify import slugify


class News(models.Model):
    title = models.CharField(max_length=50, unique=True, blank=False)
    slug = models.SlugField(blank=True)
    body = models.CharField(max_length=150, blank=False)
    image = models.ImageField(upload_to='news/', blank=True)

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
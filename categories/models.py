from django.db import models
from slugify import slugify

class Category(models.Model):
    
    class Meta:
        verbose_name_plural = 'Categories'

    title = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    slug = models.SlugField(primary_key=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.slug
    
    def save(self, *args, **kwargs): 
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    


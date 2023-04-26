from django.contrib import admin

from .models import Favorite, ForumPost

# Register your models here.
admin.site.register(Favorite)
admin.site.register(ForumPost)
from django.contrib import admin
from .models import News

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'image', 'body')
    list_display_links = ('title', 'slug')

admin.site.register(News, NewsAdmin)

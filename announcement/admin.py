from django.contrib import admin

from .models import Announcement


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'created_at', 'updated_at', 'get_today_count', 'get_month_count')
    list_filter = ('category__title', 'location')

admin.site.register(Announcement, AnnouncementAdmin)


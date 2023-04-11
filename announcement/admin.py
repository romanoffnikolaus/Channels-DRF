from django.contrib import admin

from announcement.models import Announcement, AnnouncementPhoto


class AnnouncementPhoto(admin.TabularInline):
    model = AnnouncementPhoto


@admin.register(Announcement)
class Announcement(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at')
    inlines = [AnnouncementPhoto]

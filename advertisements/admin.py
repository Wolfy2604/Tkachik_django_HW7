from django.contrib import admin

from advertisements.models import Advertisement


@admin.register(Advertisement)
class AdvAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'status', 'creator', 'created_at', 'updated_at']

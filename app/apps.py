from django.apps import AppConfig
from django.contrib import admin


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

# class AttendanceAdmin(admin.ModelAdmin):


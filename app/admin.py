from django.contrib import admin
from app.models import *

# Register your models here.
admin.site.register(Miembro)
admin.site.register(Cargo)
admin.site.register(Estado)
admin.site.register(Servicio)


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('miembro', 'date', 'present')

admin.site.register(Attendance, AttendanceAdmin)



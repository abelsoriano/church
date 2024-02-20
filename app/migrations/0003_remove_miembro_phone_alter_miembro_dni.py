# Generated by Django 4.2.4 on 2024-01-09 05:37

import app.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_attendance_service_alter_attendance_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='miembro',
            name='phone',
        ),
        migrations.AlterField(
            model_name='miembro',
            name='dni',
            field=models.BigIntegerField(blank=True, null=True, unique=True, validators=[app.models.validate_dni_length, django.core.validators.MaxLengthValidator(limit_value=11, message='El DNI debe tener 11 dígitos.')], verbose_name='CEDULA'),
        ),
    ]
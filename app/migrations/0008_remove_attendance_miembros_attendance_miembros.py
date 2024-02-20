# Generated by Django 4.2.4 on 2024-01-10 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_attendance_miembros_attendance_miembros'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='miembros',
        ),
        migrations.AddField(
            model_name='attendance',
            name='miembros',
            field=models.ManyToManyField(related_name='asistencias', to='app.miembro', verbose_name='MIEMBROS'),
        ),
    ]

# Generated by Django 4.2 on 2023-08-20 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asistencia',
            name='hora',
        ),
        migrations.AddField(
            model_name='asistencia',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='estado',
            field=models.CharField(max_length=30),
        ),
    ]

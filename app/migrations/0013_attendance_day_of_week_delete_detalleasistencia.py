# Generated by Django 4.2.4 on 2024-02-20 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_detalleasistencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='day_of_week',
            field=models.CharField(blank=True, editable=False, max_length=10, verbose_name='DÍA DE LA SEMANA'),
        ),
        migrations.DeleteModel(
            name='DetalleAsistencia',
        ),
    ]

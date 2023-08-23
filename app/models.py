from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.utils import timezone
from app.choices import gender_choices, asistencia_choices
from setting.settings import MEDIA_URL, STATIC_URL


# Create your models here.

class Estado(models.Model):
    name = models.CharField(max_length=50, verbose_name='Estado')

    def __str__(self):
        return self.name

    def toJSON(self):
        data = {
            'name': self.name,
        }
        return data

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
        db_table = 'estado'
        ordering = ['id']


class Cargo(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        db_table = 'cargo'
        ordering = ['id']


def validate_dni_length(value):
    if value is not None and (value < 10000000000 or value > 99999999999):
        raise ValidationError("La longitud del número de cédula debe ser de 11 dígitos.")


def validate_phone_prefix(value):
    if value is not None and (value < 1000000000 or value > 9999999999):
        raise ValidationError("La longitud del número de teléfono debe ser de 10 dígitos.")

    # Convierte el valor a cadena para poder comprobar el prefijo
    phone_str = str(value)

    # Verifica si el prefijo comienza con "809", "829" o "849"
    if not phone_str.startswith(("809", "829", "849")):
        raise ValidationError("El número de teléfono debe comenzar con 809, 829 o 849.")


class Miembro(models.Model):
    name = models.CharField(max_length=50, verbose_name='NOMBRE')
    lastname = models.CharField(max_length=50, verbose_name='APELLIDOS')
    dni = models.BigIntegerField(verbose_name='CEDULA', unique=True, null=True, blank=True,
                                 validators=[validate_dni_length])
    gender = models.CharField(max_length=15, choices=gender_choices, verbose_name="GENERO")
    date_joined = models.DateField(verbose_name='FECHA DE NACIMIENTO')
    address = models.CharField(max_length=150, verbose_name='DIRECCION')
    fecha_ingreso = models.DateField(verbose_name='FECHA DE INGRESO')
    phone = models.PositiveIntegerField(null=True, blank=True, verbose_name='TELEFONO',
                                        validators=[validate_phone_prefix])
    email = models.CharField(max_length=30, null=True, blank=True, verbose_name='CORREO ELECTRONICO')
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, verbose_name='CARGO')
    image = models.ImageField(upload_to='avatar', null=True, blank=True, verbose_name='IMAGEN')
    state = models.ForeignKey(Estado, on_delete=models.CASCADE, verbose_name="ESTADO")

    def read_image(self):
        if self.image:
            try:
                with self.image.open() as f:
                    return f.read()
            except FileNotFoundError:
                pass
        return None

    def __str__(self):
        return self.name + ' ' + self.lastname

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(MEDIA_URL, 'img/empty.png')

    def toJSON(self):
        data = model_to_dict(self)
        data['state'] = self.state.toJSON() if self.state else None
        data['cargo'] = self.cargo.toJSON() if self.cargo else None
        data['image'] = self.get_image()
        return data

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        db_table = 'miembro'
        ordering = ['id']


class Asistencia(models.Model):
    usuario = models.ForeignKey(Miembro, on_delete=models.CASCADE)
    estado = models.CharField(max_length=30)  # Presente, Ausente
    status = models.BooleanField(default=True)
    fecha = models.DateField(verbose_name='FECHA DE CREACION')

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        db_table = 'asistencia'
        ordering = ['id']


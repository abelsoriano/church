
from django.db import models


from django.forms import model_to_dict
from django.utils import timezone
from app.choices import *
from setting.settings import MEDIA_URL


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


# Crearte miembros
class Miembro(models.Model):
    name = models.CharField(max_length=50, verbose_name='NOMBRE')
    lastname = models.CharField(max_length=50, verbose_name='APELLIDOS')
    dni = models.CharField(max_length=13, verbose_name='CEDULA', unique=True, null=True, blank=True)
    gender = models.CharField(max_length=15, choices=gender_choices, verbose_name="GENERO")
    date_joined = models.DateField(verbose_name='FECHA DE NACIMIENTO')
    address = models.CharField(max_length=150, verbose_name='DIRECCION')
    fecha_ingreso = models.DateField(verbose_name='FECHA DE INGRESO')
    phone = models.CharField(max_length=12, null=True, blank=True, verbose_name='TELEFONO')
    email = models.CharField(max_length=30, null=True, blank=True, verbose_name='CORREO ELECTRONICO')
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, verbose_name='CARGO')
    image = models.ImageField(upload_to='avatar', null=True, blank=True, verbose_name='IMAGEN')
    state = models.ForeignKey(Estado, on_delete=models.CASCADE, verbose_name="ESTADO")
    category = models.CharField(max_length=20, choices=category_choices, verbose_name='CATEGORIA')

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



class Servicio(models.Model):
    fecha = models.DateField(default=timezone.now, verbose_name='FECHA DE SERVICIO')
    hora = models.TimeField(default=timezone.now)
    direccion = models.CharField(max_length=200, verbose_name='DIRECCION DEL CULTO DE ALTAR')
    lectura = models.TextField(verbose_name='LECTURA DE LA PALABRAS')
    devocional_1 = models.CharField(max_length=100, verbose_name='DEVOCIONAL')
    cultural = models.TextField(verbose_name='CULTURAL')
    mensaje = models.TextField(verbose_name='MENSAJE DE LAS PALABRAS')
    description = models.TextField(blank=True, null=True, verbose_name='DESCRIPCION')

    def __str__(self):
        return str(self.hora.strftime("%H:%M:%S"))

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'


class Attendance(models.Model):
    miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True, default=timezone.now, verbose_name='FECHA DE SERVICIO')
    present = models.BooleanField(default=False, null=True, blank=True, verbose_name='PRESENTE')
    day_of_week = models.CharField(max_length=10, blank=True, editable=False, verbose_name='DÍA DE LA SEMANA')

    def toJSON(self):
        data = model_to_dict(self)
        data['miembro'] = self.miembro.toJSON() if self.miembro else None
        return data

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'


class MiembroStatus(models.Model):
    miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=(
        ('enfermo', 'Miembro se encuentra enfermo'),
        ('visitar', 'Miembro necesita ser visitado'),
        ('permiso', 'Miembro tiene permiso o excusa'),

    ))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.miembro.name} - {self.status}"

    class Meta:
        verbose_name = 'StatusMiembro'
        verbose_name_plural = 'StatusMiembros'
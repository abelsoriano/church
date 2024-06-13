from datetime import datetime

from django.forms import *
from django import forms
from app.models import *


# Create Miembro
class MemberForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Miembro
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su apellido'}),
            'dni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su numero de identidad'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_joined': DateInput(format='%d/%m/%Y',
                                     attrs={'class': 'form-control datepicker', 'placeholder': 'mm/dd/yyyy'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Direccion'}),
            'fecha_ingreso': DateInput(format='%d/%m/%Y', attrs={'class': 'form-control datepicker', 'placeholder': 'mm/dd/yyyy'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese sin guión'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '@'}),
            'cargo': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if len(dni) != 13 or not dni.replace("-", "").isdigit():
            raise forms.ValidationError("El DNI debe tener el formato 000-0000000-0 y contener 11 números.")
        return dni

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) != 12 or not phone.replace("-", "").isdigit():
            raise forms.ValidationError("El teléfono debe tener el formato 000-000-0000 y contener 10 números.")
        return phone

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


# Formulario para crear servicio
class ServicioForm(ModelForm):
    class Meta:
        model = Servicio
        exclude = ['hora']
        fields = '__all__'
        widgets = {
            'fecha': DateInput(
                format='%d/%m/%Y',
                attrs={'autocomplete': 'off', 'id': 'datepicker2', 'class': 'form-control datepicker',
                       'placeholder': 'm/d/yyyy'}),
            'hora': TimeField(required=False, disabled=True),
            'direccion': TextInput(
                attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Ingrese un nombre', }),
            'lectura': TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Ingrese el libro', }),
            'devocional_1': TextInput(
                attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Ingrese un nombre', }),
            'cultural': TextInput(
                attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Ingrese un mombre', }),
            'mensaje': TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Ingrese un nombre', }),
            'description': Textarea(attrs={'class': 'form-control', 'placeholder': 'opcional', 'rows': 3}),

        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['miembro', 'date', 'present']

#
#
#
#
#

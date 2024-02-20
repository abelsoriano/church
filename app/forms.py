from datetime import datetime

from django.forms import *
from django import forms
from app.models import *


# Create Miembro
class MemberForm(ModelForm):
    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Miembro
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    # 'id': 'validationCustom01',
                    # 'required': True,
                    'placeholder': 'Ingrese un nombre',

                }
            ),

            'lastname': TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',

                    'placeholder': 'Ingrese su apellido',
                }
            ),
            'dni': NumberInput(
                attrs={
                    'type': 'number',
                    'class': 'form-control',
                    'placeholder': 'Ingresar su numero de identidad',
                }
            ),
            'gender': Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su genero',
                }
            ),

            'date_joined': DateInput(
                format='%d/%m/%Y',
                attrs={'autocomplete': 'off', 'id': 'datepicker2', 'class': 'form-control datepicker',
                       'placeholder': 'm/d/yyyy',

                       }
            ),

            'state': Select(attrs={'class': 'form-control', }),
            'address': TextInput(attrs={'class': 'form-control', 'placeholder': 'Direccion'}),
            'fecha_ingreso': DateInput(format='%d/%m/%Y', attrs={  # 'value': datetime.now().strftime('%m/%d/%Y'),
                'autocomplete': 'off', 'id': 'datepicker', 'class': 'form-control datepicker',
                'placeholder': 'm/d/yyyy'}),
            'phone': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese sin guión'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': '@mail.hotmail.outlook'}),
            'cargo': Select(attrs={'class': 'form-control', 'class': 'form-control select2'}),
            'category': Select(attrs={'class': 'form-control', }),
            'image': FileInput(attrs={'class': 'form-control'})

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

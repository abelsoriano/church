# signals.py

from django.db.models.signals import post_save
from django.utils import timezone
from .models import Miembro
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib import messages

@receiver(post_save, sender=Miembro)
def birthday_notification(sender, instance, created, **kwargs):
    if created:
        # Verificar si el miembro cumple años hoy
        today = timezone.now().date()
        if instance.date_joined.month == today.month and instance.date_joined.day == today.day:
            # Aquí debes escribir el código para enviar la notificación
            # Puedes usar cualquier método de notificación que desees, como enviar un correo electrónico, una notificación push, etc.
            # Por ejemplo, si tienes un método de notificación por correo electrónico, puedes llamarlo así:
            send_birthday_email(instance)

# En el mismo archivo signals.py o en otro archivo de utilidades

def send_birthday_email(miembro):
    # Aquí debes escribir el código para enviar el correo electrónico de notificación
    # Por ejemplo:
    subject = "¡Feliz Cumpleaños!"
    message = "¡Feliz Cumpleaños, {}! Esperamos que tengas un día maravilloso.".format(miembro.name)
    # Código para enviar el correo electrónico usando Django's send_mail() o cualquier otro método que estés usando para enviar correos electrónicos.

# signals.py



@receiver(user_logged_in)
def show_popup_on_login(sender, user, request, **kwargs):
    # Aquí puedes agregar lógica para determinar cuándo mostrar la ventana emergente
    # Por ejemplo, puedes mostrarla siempre que un usuario inicie sesión correctamente.
    messages.info(request, '¡Bienvenido de nuevo, {}!'.format(user.first_name + user.last_name))

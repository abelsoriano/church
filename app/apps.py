from django.apps import AppConfig

class MiappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        # Importar señales
        import app.signals


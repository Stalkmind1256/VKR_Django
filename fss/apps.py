from django.apps import AppConfig


class FssConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fss'

    def ready(self):
        import fss.signals  # Импорт сигналов при старте

from django.apps import AppConfig

class ActionappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'actionapp'

    def ready(self):
        import actionapp.signals
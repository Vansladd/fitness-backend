from django.apps import AppConfig


class StepsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "steps"
    def ready(self):
        import steps.signals

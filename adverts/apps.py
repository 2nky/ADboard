from django.apps import AppConfig


class AdvertsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "adverts"

    def ready(self):
        # Это нужно чтобы сигналы работали
        from . import signals

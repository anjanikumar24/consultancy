from django.apps import AppConfig
from django.db.models.signals import post_migrate


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Website content"

    def ready(self):
        from .seed import seed_defaults
        post_migrate.connect(seed_defaults, sender=self, dispatch_uid="core_seed_defaults")

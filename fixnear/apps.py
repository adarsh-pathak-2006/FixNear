from django.apps import AppConfig


class FixnearConfig(AppConfig):
    name = 'fixnear'
    verbose_name = 'FixNear Core'

    def ready(self):
        import fixnear.signals  # noqa: F401

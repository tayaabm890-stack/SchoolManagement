
from django.apps import AppConfig


class SchoolappConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'

    name = 'schoolapp'

    def ready(self):

        import schoolapp.signals


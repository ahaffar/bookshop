from django.apps import AppConfig


class RentalConfig(AppConfig):
    name = 'rental'

    def ready(self):
        try:
            import rental.signals
        except ImportError:
            pass

from django.apps import AppConfig

# Configuration class for the 'mybank' app. 
class MybankConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mybank'

    # Import the signals module(signals.py) to register signal handlers
    def ready(self):
        import mybank.signals

from django.apps import AppConfig


class EcommerceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecommerce'

    def ready(self):
        """Add a signal so that when the application starts, the signal is activated"""
        import ecommerce.signals

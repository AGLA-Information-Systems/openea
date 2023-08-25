from django.apps import AppConfig


class AuthorizationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authorization'

    def ready(self):
        # you must import your modules here 
        # to avoid AppRegistryNotReady exception
        # startup code here
        pass

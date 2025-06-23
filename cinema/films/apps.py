from django.apps import AppConfig


class FilmsConfig(AppConfig):
    """
    Configuration class for the 'films' Django application.

    Attributes:
        default_auto_field (str): Specifies the type of auto-created primary key field.
        name (str): The full Python path to the application.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "films"

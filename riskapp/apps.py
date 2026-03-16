from django.apps import AppConfig


class RiskappConfig(AppConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'
    name = 'riskapp'

from django.apps import AppConfig

"""
Application configuration for the 'api' app.

This class defines default settings for the app, including
the type of primary key used for new models and the app name
registered within Django.
"""
class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
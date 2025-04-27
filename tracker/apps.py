"""
Application configuration for the Health Tracker app.

This file contains the TrackerConfig class which configures
the tracker application and its metadata.
"""

from django.apps import AppConfig

class TrackerConfig(AppConfig):
    """
    Configuration class for the tracker application.

    Provides metadata and configuration options for the health tracker app.
    """
    
    # Default auto field to use for models in this app
    # Using BigAutoField as the default for model primary keys
    default_auto_field = "django.db.models.BigAutoField"
    
    # Name of the application (Python path)
    name = "tracker"
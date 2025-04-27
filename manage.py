#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

This script serves as the entry point for:
- Running the development server
- Executing management commands
- Managing database migrations
- Interacting with your Django project

For more information, see:
https://docs.djangoproject.com/en/4.2/ref/django-admin/
"""

import os
import sys


def main():
    """
    Execute Django administrative tasks.
    
    Sets up the environment and executes commands from the command line.
    """
    # Set the default Django settings module for the 'health_tracker' project
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "health_tracker.settings")

    try:
        # Try to import Django's execute_from_command_line function
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Provide helpful error messages if Django isn't available
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Execute the command line arguments
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    # Run the main function when executed directly
    main()
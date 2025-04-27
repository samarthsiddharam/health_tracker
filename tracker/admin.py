"""
Admin configuration for the Health Tracker application.

This file registers models with the Django admin interface and customizes
how they are displayed and interacted with in the admin panel.
"""

from django.contrib import admin
from .models import HealthRecord

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for HealthRecord model.
    
    Customizes how health records are displayed and filtered in the Django admin panel.
    """
    
    # Fields to display in the list view of admin panel
    list_display = (
        'user',          # The user who created the record
        'date',          # Date of the health record
        'steps',         # Number of steps recorded
        'water_intake_ml',  # Water intake in milliliters
        'sleep_hours'    # Hours of sleep recorded
    )
    
    # Fields available for filtering the records in admin panel
    list_filter = (
        'date',  # Filter records by date
        'user'   # Filter records by user
    )
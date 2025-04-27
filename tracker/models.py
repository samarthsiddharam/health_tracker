"""
Database models for the Health Tracker application.

This module defines the data structure for storing health records
and their relationships with users.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class HealthRecord(models.Model):
    """
    Represents a daily health record containing:
    - Step count
    - Water intake
    - Sleep duration
    
    Each record is associated with a specific user and date.
    """

    # Reference to the user who created this record
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # Delete records when user is deleted
        related_name='health_records'  # Access records via user.health_records
    )

    # Date of the health record (defaults to current date)
    date = models.DateField(
        default=timezone.now,  # Set to current date when record is created
        help_text="Date of the health record"
    )

    # Number of steps taken (must be positive or zero)
    steps = models.PositiveIntegerField(
        default=0,
        help_text="Number of steps taken"
    )

    # Water intake in milliliters (must be positive or zero)
    water_intake_ml = models.PositiveIntegerField(
        default=0,
        help_text="Water intake in milliliters"
    )

    # Hours of sleep (can include fractions of hours)
    sleep_hours = models.FloatField(
        default=0,
        help_text="Hours of sleep"
    )

    class Meta:
        # Ensure each user has only one record per date
        unique_together = ('user', 'date')
        # Default ordering by date (newest first)
        ordering = ['-date']

    def __str__(self):
        """Human-readable representation of the health record."""
        return f"{self.user.username}'s record on {self.date.strftime('%Y-%m-%d')}"

    @property
    def sleep_minutes(self):
        """Return sleep duration in minutes (converted from hours)."""
        return int(self.sleep_hours * 60)
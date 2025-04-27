"""
Forms for the Health Tracker application.

This module contains form classes that handle user input validation
and data processing for the health tracker functionality.
"""

from django import forms
from django.utils import timezone
from .models import HealthRecord
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class HealthRecordForm(forms.ModelForm):
    """
    Form for creating and updating health records.

    Handles validation and display of health record data including:
    - Date of record
    - Step count
    - Water intake
    - Sleep hours
    """

    class Meta:
        model = HealthRecord
        fields = ['date', 'steps', 'water_intake_ml', 'sleep_hours']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date'  # Use HTML5 date picker
            }),
            'steps': forms.NumberInput(attrs={
                'min': '0'  # Ensure step count can't be negative
            }),
            'water_intake_ml': forms.NumberInput(attrs={
                'min': '0'  # Ensure water intake can't be negative
            }),
            'sleep_hours': forms.NumberInput(attrs={
                'min': '0',       # Ensure sleep hours can't be negative
                'step': '0.25'     # Allow quarter-hour increments
            }),
        }

    def __init__(self, *args, **kwargs):
        """Initialize the form with current date as default."""
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = timezone.localdate()

    def clean_date(self):
        """
        Validate that the record date is not in the future.
        
        Raises:
            forms.ValidationError: If date is in the future
        
        Returns:
            date: The validated date
        """
        date = self.cleaned_data['date']
        if date > timezone.localdate():
            raise forms.ValidationError("Date cannot be in the future")
        return date


class RegisterForm(UserCreationForm):
    """
    User registration form extending Django's built-in UserCreationForm.

    Handles new user registration with username and password fields.
    Includes built-in password validation from UserCreationForm.
    """

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
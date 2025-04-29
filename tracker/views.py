"""
Views for the Health Tracker application.

This module contains all the view functions that handle:
- User authentication (registration)
- Health record management (CRUD operations)
- Data export functionality (CSV, PDF)
- Dashboard display with analytics
"""

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponse
import csv
from django.utils import timezone
from reportlab.pdfgen import canvas
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from datetime import timedelta
import json

from .forms import HealthRecordForm, RegisterForm
from .models import HealthRecord

@login_required
def dashboard(request):
    """
    Display the user's dashboard with health records and analytics.
    
    Shows:
    - All historical records (newest first)
    - Latest record summary
    - Chart data for the last 7 days
    """
    # Get all records for the current user, ordered by date (newest first)
    records = HealthRecord.objects.filter(user=request.user).order_by('-date')
    
    # Get the latest record or None if no records exist
    latest_record = records.first()
    
    # Get data for the last 7 days for the chart
    date_from = timezone.now().date() - timedelta(days=7)
    chart_data = HealthRecord.objects.filter(
        user=request.user,
        date__gte=date_from
    ).order_by('date')
    
    # Prepare context with both Python objects and JSON serialized data
    context = {
        'records': records,
        'latest_record': latest_record,
        'current_date': timezone.now(),
        'records_json': json.dumps([{
            'date': record.date.strftime('%Y-%m-%d'),
            'steps': record.steps,
            'water_intake_ml': record.water_intake_ml,
            'sleep_hours': record.sleep_hours
        } for record in records]),
        'latest_record_json': json.dumps({
            'steps': latest_record.steps if latest_record else 0,
            'water_intake_ml': latest_record.water_intake_ml if latest_record else 0,
            'sleep_hours': latest_record.sleep_hours if latest_record else 0,
            'date': latest_record.date.strftime('%Y-%m-%d') if latest_record else ''
        }),
        'chart_data_json': json.dumps([{
            'date': record.date.strftime('%Y-%m-%d'),
            'steps': record.steps,
            'water_intake_ml': record.water_intake_ml,
            'sleep_hours': record.sleep_hours
        } for record in chart_data])
    }
    
    return render(request, 'tracker/dashboard.html', context)

@login_required
def add_record(request):
    """
    Handle creation of new health records.
    
    GET: Display empty form
    POST: Validate and save new record
    """
    if request.method == 'POST':
        form = HealthRecordForm(request.POST)
        if form.is_valid():
            # Save record with current user
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            messages.success(request, 'Record added successfully!')
            return redirect('dashboard')
    else:
        form = HealthRecordForm()
    
    return render(request, 'tracker/add_record.html', {'form': form})

def register(request):
    """
    Handle new user registration.
    
    Includes password strength validation and automatic login after registration.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                # Validate password meets strength requirements
                validate_password(form.cleaned_data['password1'], user=form.instance)
                user = form.save()
                login(request, user)  # Automatically log in the new user
                return redirect('dashboard')
            except ValidationError as e:
                # Add password validation errors to form
                form.add_error('password1', e)
    else:
        form = RegisterForm()
        
    return render(request, 'tracker/register.html', {'form': form})

@login_required
def export_csv(request):
    """
    Export all health records as CSV file.
    
    Returns:
        HttpResponse: CSV file download
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="health_data.csv"'
    
    writer = csv.writer(response)
    # Write CSV header
    writer.writerow(['Date', 'Steps', 'Water (ml)', 'Sleep (hrs)'])
    
    # Write all records as CSV rows
    records = HealthRecord.objects.filter(user=request.user)
    for record in records:
        writer.writerow([
            record.date,
            record.steps,
            record.water_intake_ml,
            record.sleep_hours
        ])
    
    return response

@login_required
def export_pdf(request):
    """
    Export all health records as PDF file.
    
    Returns:
        HttpResponse: PDF file download
    """
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="health_data.pdf"'
    
    # Create PDF document
    p = canvas.Canvas(response)
    p.drawString(100, 800, "Your Health Data")
    
    # Write each record as a line in the PDF
    records = HealthRecord.objects.filter(user=request.user)
    y = 750  # Vertical position tracker
    for record in records:
        p.drawString(100, y, 
            f"{record.date}: "
            f"{record.steps} steps, "
            f"{record.water_intake_ml} ml, "
            f"{record.sleep_hours} hrs"
        )
        y -= 20  # Move down for next record
    
    p.showPage()
    p.save()
    return response
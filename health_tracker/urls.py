"""
URL configuration for health_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from tracker.views import dashboard, add_record, register, export_csv, export_pdf, create_superuser_view
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

# Main URL patterns for the health tracker application
urlpatterns = [
    # Temporary for creating Superuser
    path('create-superuser/', create_superuser_view),

    # Admin interface URL
    path('admin/', admin.site.urls),
    
    # Dashboard - main page of the application
    path('', dashboard, name='dashboard'),
    
    # Add new health record
    path('add/', add_record, name='add_record'),
    
    # User registration
    path('register/', register, name='register'),
    
    # User logout (using Django's built-in LogoutView)
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Export data to CSV
    path('export/csv/', export_csv, name='export_csv'),
    
    # Export data to PDF
    path('export/pdf/', export_pdf, name='export_pdf'),
    
    # Include Django's built-in auth URLs for:
    # - login (/accounts/login/)
    # - password change (/accounts/password_change/)
    # - password reset (/accounts/password_reset/)
    # etc.
    path('accounts/', include('django.contrib.auth.urls')),
]

# Serve static and media files during development only
if settings.DEBUG:
    # Static files (CSS, JavaScript, Images)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Media files (user-uploaded content)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
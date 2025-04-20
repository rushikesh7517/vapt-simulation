# scanner/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.nmap_scan_view, name='nmap_scan'),
]

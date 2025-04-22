# scanner/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dmitry_scan_view, name='dmitry_scan'),
]

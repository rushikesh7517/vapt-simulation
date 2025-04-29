from django.urls import path
from . import views

urlpatterns = [
    path('', views.harvester_scan_view, name='harvester_scan'),
]

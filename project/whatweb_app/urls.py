from django.urls import path
from . import views

urlpatterns = [
    path('', views.whatweb_scan_view, name='whatweb_scan'),
]

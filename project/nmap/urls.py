from django.urls import path

from . import views

urlpatterns = [
    path('', views.nmap_home),
    path('result', views.nmap_result),
]

"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),         # Onboarding and dashboard
    path('accounts/', include('accounts.urls')), # Login, Register, Logout
    path('nmap/', include('nmap.urls')),          # Nmap Scanner
    path('dmitry/', include('dmitry.urls')),      # Dmitry Scanner
    path('bruteforce/', include('bruteforce.urls')), # Brute Force Scanner
    path('theharvester/', include('theharvester.urls')), # theHarvester
    path('whatweb/', include('whatweb_app.urls')),  #whatweb_app

]


from django.urls import path
from .views import onboarding_view, dashboard_view

urlpatterns = [
    path('', onboarding_view, name='onboarding'),      # Landing
    path('home/', dashboard_view, name='dashboard'),    # After login Dashboard
]


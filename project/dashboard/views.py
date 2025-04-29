from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def onboarding_view(request):
    return render(request, 'dashboard/onboarding.html')

@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')

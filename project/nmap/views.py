# scanner/views.py
from django.shortcuts import render
from .forms import NmapScanForm
import subprocess
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def your_scanner_view(request):
    ...

def nmap_scan_view(request):
    form = NmapScanForm()
    if request.method == 'POST':
        form = NmapScanForm(request.POST)
        if form.is_valid():
            target = form.cleaned_data['target']
            options = form.cleaned_data['options']
            cmd = ['nmap'] + options + [target]

            try:
                result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
            except subprocess.CalledProcessError as e:
                result = e.output

            # No file saving - just pass results to the template
            context = {
                'target': target,
                'options': ' '.join(options),
                'result': result
            }
            return render(request, 'nmap/result.html', context)

    return render(request, 'nmap/nmap.html', {'form': form})
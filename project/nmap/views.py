# scanner/views.py
from django.shortcuts import render
from .forms import NmapScanForm
import subprocess

def nmap_scan_view(request):
    form = NmapScanForm()
    if request.method == 'POST':
        form = NmapScanForm(request.POST)
        if form.is_valid():
            target = form.cleaned_data['target']
            options = form.cleaned_data['options']
            cmd = ['nmap'] + options + [target]
            try:
                print(f"[DEBUG] Running command: {' '.join(cmd)}")
                result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
                print("[NMAP RESULT]")
                print(result)
            except subprocess.CalledProcessError as e:
                print("[ERROR]")
                print(e.output)

    return render(request, 'nmap/nmap.html', {'form': form})

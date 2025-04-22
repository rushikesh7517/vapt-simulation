# scanner/views.py
from django.shortcuts import render
from .forms import NmapScanForm
import subprocess
import os
from django.conf import settings
from datetime import datetime

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

            # Save result to file
            scans_dir = os.path.join(settings.BASE_DIR, 'scans')
            os.makedirs(scans_dir, exist_ok=True)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_target = target.replace('.', '_').replace(':', '_').replace('/', '_')
            filename = f"nmap_{safe_target}_{timestamp}.txt"
            filepath = os.path.join(scans_dir, filename)

            with open(filepath, 'w') as f:
                f.write(f"Nmap Scan Report for {target}\n")
                f.write(f"Options: {' '.join(options)}\n\n")
                f.write(result)

            context = {
                'target': target,
                'options': ' '.join(options),
                'result': result,
                'file_path': filename
            }
            return render(request, 'nmap/result.html', context)

    return render(request, 'nmap/nmap.html', {'form': form})

from django.shortcuts import render
from .forms import DmitryScanForm
import subprocess
import os
from django.conf import settings
from datetime import datetime
def dmitry_scan_view(request):
    form = DmitryScanForm()
    if request.method == 'POST':
        form = DmitryScanForm(request.POST)
        if form.is_valid():
            target = form.cleaned_data['target']
            options = form.cleaned_data['options']
            cmd = ['dmitry'] + options + [target]

            try:
                result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
            except subprocess.CalledProcessError as e:
                result = e.output

            context = {
                'target': target,
                'options': ' '.join(options),
                'result': result
            }
            return render(request, 'dmitry/result.html', context)

    return render(request, 'dmitry/dmitry.html', {'form': form})


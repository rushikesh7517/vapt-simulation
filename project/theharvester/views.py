from django.shortcuts import render
import subprocess
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def harvester_scan_view(request):
    if request.method == 'POST':
        target = request.POST.get('target')
        source = request.POST.get('source')
        limit = request.POST.get('limit')

        # theHarvester command
        cmd = [
            'theHarvester',
            '-d', target,
            '-b', source,
            '-l', limit
        ]

        try:
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            result = e.output

        context = {
            'result': result,
            'target': target,
            'source': source
        }
        return render(request, 'theharvester/result.html', context)

    return render(request, 'theharvester/harvester.html')

from django.shortcuts import render
import subprocess, os
from datetime import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def harvester_scan_view(request):
    if request.method == 'POST':
        target = request.POST['target']
        source = request.POST['source']
        limit = request.POST['limit']

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

        # Save Result to File
        harvest_dir = os.path.join(settings.BASE_DIR, 'harvest_results')
        os.makedirs(harvest_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_target = target.replace('.', '_')
        filename = f"harvest_{safe_target}_{timestamp}.txt"
        filepath = os.path.join(harvest_dir, filename)

        with open(filepath, 'w') as f:
            f.write(f"Scan Report for: {target} using {source}\n\n")
            f.write(result)

        context = {
            'result': result,
            'target': target,
            'source': source,
            'file_path': filename
        }
        return render(request, 'theharvester/result.html', context)

    return render(request, 'theharvester/harvester.html')


from django.shortcuts import render
import subprocess
from django.contrib.auth.decorators import login_required

# ✅ Define supported sources
VALID_SOURCES = {
    'anubis', 'baidu', 'bing', 'brave', 'crtsh',
    'duckduckgo', 'rapiddns', 'sitedossier',
    'threatminer', 'urlscan', 'yahoo'
}

@login_required(login_url='login')
def harvester_scan_view(request):
    if request.method == 'POST':
        target = request.POST.get('target')
        source = request.POST.get('source', '').lower()
        limit = request.POST.get('limit')

        if source not in VALID_SOURCES:
            result = (
                f"[!] Source '{source}' is not supported by theHarvester.\n\n"
                f"✅ Supported sources: {', '.join(sorted(VALID_SOURCES))}"
            )
        else:
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

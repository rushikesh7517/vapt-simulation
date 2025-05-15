import subprocess
import re
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def whatweb_scan_view(request):
    if request.method == 'POST':
        target = request.POST.get('target')
        result = ""
        summary = {}

        try:
            cmd = ['whatweb', target]
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)

            # Strip ANSI colors
            result_clean = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', result)

            # Extract fields using regex
            summary['Status'] = re.search(r'\[(\d{3} .+?)\]', result_clean)
            summary['Status'] = summary['Status'].group(1) if summary['Status'] else "N/A"

            summary['IP'] = re.search(r'IP\[(.*?)\]', result_clean)
            summary['IP'] = summary['IP'].group(1) if summary['IP'] else "N/A"

            summary['Country'] = re.search(r'Country\[(.*?)\]', result_clean)
            summary['Country'] = summary['Country'].group(1) if summary['Country'] else "N/A"

            summary['Server'] = re.search(r'HTTPServer\[(.*?)\]', result_clean)
            summary['Server'] = summary['Server'].group(1) if summary['Server'] else "N/A"

            summary['Title'] = re.search(r'Title\[(.*?)\]', result_clean)
            summary['Title'] = summary['Title'].group(1) if summary['Title'] else "N/A"

            summary['Headers'] = re.search(r'UncommonHeaders\[(.*?)\]', result_clean)
            summary['Headers'] = summary['Headers'].group(1) if summary['Headers'] else "N/A"

        except subprocess.CalledProcessError as e:
            result = e.output
            summary = {"Error": "Scan failed or site is protected."}

        context = {
            'target': target,
            'result': result,
            'summary': summary
        }
        return render(request, 'whatweb_app/result.html', context)

    return render(request, 'whatweb_app/scan.html')

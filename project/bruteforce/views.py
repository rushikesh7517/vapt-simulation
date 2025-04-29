from .forms import BruteForceForm
import subprocess, os
from datetime import datetime
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def your_scanner_view(request):
    ...



def brute_force_view(request):
    form = BruteForceForm()
    if request.method == 'POST':
        form = BruteForceForm(request.POST, request.FILES)
        if form.is_valid():
            target_ip = form.cleaned_data['target_ip']
            user_file = request.FILES['username_wordlist']
            pass_file = request.FILES['password_wordlist']

            # Save uploaded files temporarily
            upload_dir = os.path.join(settings.BASE_DIR, 'temp_wordlists')
            os.makedirs(upload_dir, exist_ok=True)

            user_path = os.path.join(upload_dir, f"userlist_{user_file.name}")
            pass_path = os.path.join(upload_dir, f"passlist_{pass_file.name}")

            with open(user_path, 'wb+') as dest:
                for chunk in user_file.chunks():
                    dest.write(chunk)

            with open(pass_path, 'wb+') as dest:
                for chunk in pass_file.chunks():
                    dest.write(chunk)

            # Run hydra with uploaded files
            cmd = ['hydra', '-L', user_path, '-P', pass_path, f'ssh://{target_ip}']

            try:
                result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
            except subprocess.CalledProcessError as e:
                result = e.output

            # Detect matched credentials
            matched_lines = [line.strip() for line in result.splitlines() if 'login:' in line and 'password:' in line]
            found_credentials = '\n'.join(matched_lines)

            # Save result to file
            brute_dir = os.path.join(settings.BASE_DIR, 'brute_results')
            os.makedirs(brute_dir, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"brute_{target_ip.replace('.', '_')}_{timestamp}.txt"
            filepath = os.path.join(brute_dir, filename)

            with open(filepath, 'w') as f:
                f.write(f"Target IP: {target_ip}\n")
                f.write(f"Userlist: {user_path}\n")
                f.write(f"Passlist: {pass_path}\n\n")
                f.write(result)

            context = {
                'result': result,
                'file_path': filename,
                'target_ip': target_ip,
                'matched': found_credentials or None
            }
            return render(request, 'bruteforce/result.html', context)

    return render(request, 'bruteforce/bruteforce.html', {'form': form})

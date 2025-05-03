from .forms import BruteForceForm
import subprocess
import tempfile
import os
from django.shortcuts import render
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

            user_path = None
            pass_path = None
            temp_files = [] # To keep track of temporary files to clean up

            try:
                # Determine source of usernames: text input or file upload
                usernames_input = form.cleaned_data.get('usernames_input') # Assuming you add this field to your form
                if usernames_input:
                    with tempfile.NamedTemporaryFile(delete=False, mode='w') as user_temp:
                        user_temp.write(usernames_input)
                        user_path = user_temp.name
                        temp_files.append(user_path)
                elif 'username_wordlist' in request.FILES:
                    user_file = request.FILES['username_wordlist']
                    with tempfile.NamedTemporaryFile(delete=False) as user_temp:
                         for chunk in user_file.chunks():
                             user_temp.write(chunk)
                         user_path = user_temp.name
                         temp_files.append(user_path)


                # Determine source of passwords: text input or file upload
                passwords_input = form.cleaned_data.get('passwords_input') # Assuming you add this field to your form
                if passwords_input:
                    with tempfile.NamedTemporaryFile(delete=False, mode='w') as pass_temp:
                        pass_temp.write(passwords_input)
                        pass_path = pass_temp.name
                        temp_files.append(pass_path)
                elif 'password_wordlist' in request.FILES:
                    pass_file = request.FILES['password_wordlist']
                    with tempfile.NamedTemporaryFile(delete=False) as pass_temp:
                         for chunk in pass_file.chunks():
                             pass_temp.write(chunk)
                         pass_path = pass_temp.name
                         temp_files.append(pass_path)


                # Ensure at least one source of usernames and passwords was provided
                if not user_path or not pass_path:
                     context = {
                        'target_ip': target_ip,
                        'error': "Please provide usernames and passwords either via text input or file upload.",
                        'success': False
                     }
                     return render(request, 'bruteforce/result.html', context)

                # Run hydra with the chosen username and password sources
                cmd = ['hydra', '-L', user_path, '-P', pass_path, '-t', '4', '-V', f'ssh://{target_ip}']

                result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, timeout=300)

                # Extract credentials from output
                matched_lines = []
                for line in result.splitlines():
                    if 'login:' in line and 'password:' in line:
                        matched_lines.append(line.strip())

                found_credentials = '\n'.join(matched_lines) if matched_lines else "No credentials found."

                context = {
                    'result': result,
                    'target_ip': target_ip,
                    'matched': found_credentials,
                    'success': True
                }

            except subprocess.CalledProcessError as e:
                context = {
                    'result': e.output,
                    'target_ip': target_ip,
                    'error': "Error executing Hydra command",
                    'success': False
                }
            except subprocess.TimeoutExpired:
                context = {
                    'target_ip': target_ip,
                    'error': "Hydra scan timed out after 5 minutes. Try with smaller wordlists or fewer inputs.",
                    'success': False
                }
            except Exception as e:
                context = {
                    'target_ip': target_ip,
                    'error': f"Unexpected error: {str(e)}",
                    'success': False
                }
            finally:
                # Clean up temporary files
                for f_path in temp_files:
                    try:
                        os.unlink(f_path)
                    except:
                        pass  # Already deleted or not accessible

            return render(request, 'bruteforce/result.html', context)

    return render(request, 'bruteforce/bruteforce.html', {'form': form})
from django import forms
class BruteForceForm(forms.Form):
    target_ip = forms.CharField(label='Target IP', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'e.g. 192.168.1.10'
    }))
    username_wordlist = forms.FileField(label='Username Wordlist')
    password_wordlist = forms.FileField(label='Password Wordlist')

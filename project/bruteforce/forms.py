from django import forms

class BruteForceForm(forms.Form):
    target_ip = forms.GenericIPAddressField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-dark text-light border-info'
        })
    )
    username_wordlist = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control bg-dark text-light border-info'
        })
    )
    password_wordlist = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control bg-dark text-light border-info'
        })
    )

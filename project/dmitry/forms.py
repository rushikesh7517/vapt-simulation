from django import forms
DMITRY_OPTIONS = [
    ('-i', 'Get IP address of host'),
    ('-w', 'Whois lookup on domain'),
    ('-n', 'Netcraft.com information'),
    ('-s', 'Search for subdomains'),
    ('-e', 'Search for email addresses'),
    ('-p', 'TCP port scan'),
]

class DmitryScanForm(forms.Form):
    target = forms.CharField(label='Target IP or Domain', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'e.g. example.com'
    }))
    options = forms.MultipleChoiceField(
        choices=DMITRY_OPTIONS,
        widget=forms.CheckboxSelectMultiple(),
        label='Dmitry Scan Options'
    )

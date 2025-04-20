from django import forms

NMAP_OPTIONS = [
    ('-sS', 'TCP SYN Scan'),
    ('-sT', 'TCP Connect Scan'),
    ('-sU', 'UDP Scan'),
    ('-sV', 'Service Version Detection'),
    ('-O', 'OS Detection'),
    ('-A', 'Aggressive Scan'),
    ('-T4', 'Faster Execution'),
    ('-Pn', 'No Ping'),
    ('-p 1-1000', 'Top 1000 Ports'),
]

class NmapScanForm(forms.Form):
    target = forms.CharField(label='Target IP or Domain', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'e.g. 192.168.1.1 or example.com'
    }))
    options = forms.MultipleChoiceField(
        choices=NMAP_OPTIONS,
        widget=forms.CheckboxSelectMultiple(),
        label='Scan Options'
    )

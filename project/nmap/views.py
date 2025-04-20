from django.shortcuts import render

def nmap_home(request):
    return render(request, "nmap/nmap_scan.html")

def nmap_result(request):
    # python code
    return render(request, "nmap/result.html")
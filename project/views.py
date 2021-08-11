from django.shortcuts import render

def error_404(request, exception):
    context ={}
    return render(request, 'landing/error_404.html', context)

def error_403(request, exception):
    context ={}
    return render(request, 'landing/error_403.html', context)

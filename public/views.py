from django.shortcuts import render

def home(request):
    return render(request, 'public/home.html')

def servicios(request):
    return render(request, 'public/servicio.html')

def contacto(request):
    return render(request, 'public/contacto.html')
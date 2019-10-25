from django.shortcuts import render
from django.http import HttpResponse
from app.models import *

# Create your views here.

def home(request):
    return render(request, 'home.html')

def admin_rutas(request):
    rutas = Ruta.objects.all()
    print(rutas)
    return render(request, 'admRutas.html', {'rutas':rutas})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *


# View Pilihan Akses & Menu

def pilih_akses(request):
    return render(request, 'access.html')

def pilih_menu(request):
    return render(request, 'akademik/menu.html')

def menu_data(request):
    if request.user.is_superuser:
        return render(request, 'data/menu.html')
    else:
        return redirect('home')

    

# View Home / Beranda

@login_required
def home_view(request):
    return render(request, 'home.html')

def handler403(request):
    return render(request, '403.html')

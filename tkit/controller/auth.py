from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from tkit.forms import *
from tkit.models import *


# Helper: Admin Access Check
def is_admin(user):
    return user.is_superuser  
 
# View: Register Orang Tua
def register_ortu(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomRegister_Ortu(request.POST)
        if form.is_valid():
            user = form.save()
            siswa = form.cleaned_data.get('nisn_siswa')
            nomor_hp = form.cleaned_data.get('nomor_hp')
            alamat = form.cleaned_data.get('alamat')

            OrangTuaMurid.objects.create(
                user=user,
                nomor_hp=nomor_hp,
                alamat=alamat,
                siswa=siswa
            )

            messages.success(request, 'Akun berhasil dibuat! Silakan login.')
            return redirect('login')
        else:
            messages.error(request, 'Terjadi kesalahan pada pendaftaran.')
    else:
        form = CustomRegister_Ortu()

    return render(request, 'auth/register_ortu.html', {'form': form})
 
# View: Login Orang Tua
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username_or_email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error('username', "Username atau password salah.")
        else:
            form.add_error(None, "Form tidak valid.")
    else:
        form = CustomLoginForm()

    return render(request, 'auth/login_ortu.html', {'form': form})
 
# View: Logout
def logout_view(request):
    logout(request)
    return redirect('access')

# View: Tambah Guru (Admin Only)
@user_passes_test(is_admin)
def tambah_guru(request):
    if request.method == 'POST':
        form = AddGuruForm(request.POST)
        if form.is_valid():
            user = form.save()

            nuptk = form.cleaned_data.get('nuptk')
            tempat_lahir = form.cleaned_data.get('tempat_lahir')
            tanggal_lahir = form.cleaned_data.get('tanggal_lahir')
            pendidikan_terakhir = form.cleaned_data.get('pendidikan_terakhir')
            nomor_hp = form.cleaned_data.get('nomor_hp')
            jabatan = form.cleaned_data.get('jabatan')
            tmt = form.cleaned_data.get('tmt')

            ProfileGuru.objects.create(
                user=user,
                nuptk=nuptk,
                tempat_lahir=tempat_lahir,
                tanggal_lahir=tanggal_lahir,
                pendidikan_terakhir=pendidikan_terakhir,
                nomor_hp=nomor_hp,
                jabatan=jabatan,
                tmt=tmt
            )

            messages.success(request, 'Akun berhasil dibuat! Silakan login untuk melanjutkan.')
            return redirect('data_guru')
        else:
            messages.error(request, 'Terjadi kesalahan dalam pendaftaran. Periksa kembali input Anda.')
    else:
        form = AddGuruForm()

    return render(request, 'auth/add_guru.html', {'form': form})

# View: Login Guru
def login_guru(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username_or_email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error('username', "Username atau password salah.")
        else:
            form.add_error(None, "Form tidak valid.")
    else:
        form = CustomLoginForm()

    return render(request, 'auth/login_guru.html', {'form': form})

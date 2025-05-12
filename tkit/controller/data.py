from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.db.models import Q, Value 
from django.db.models.functions import Concat
from tkit.models import DataSiswa, ProfileGuru, OrangTuaMurid
from tkit.forms import *


@login_required
def data_siswa(request):
    if request.user.is_staff:
        query = request.GET.get('siswa', '')
        if query:
            data_siswa = DataSiswa.objects.filter(
                Q(nama_lengkap__icontains=query) |
                Q(nis__icontains=query) |
                Q(nisn__icontains=query) 
            )
        else:
            data_siswa = DataSiswa.objects.all()
        return render(request, 'data/siswa/data_siswa.html', {
            'data_siswa': data_siswa,
            'query': query,
        })
    else:
        return redirect('home')

@login_required
def detail_siswa(request, id):
    if request.user.is_staff:
        siswa = get_object_or_404(DataSiswa, pk=id)
        return render(request, 'data/siswa/detail_siswa.html', {'siswa': siswa})
    else:
        return redirect('home')

@login_required
def tambah_siswa(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = AddSiswaForm(request.POST)
            if form.is_valid():
                form.save()

                action = request.POST.get('action')
                if action == 'save_add':
                    messages.success(request, "Data berhasil disimpan. Silakan tambah lagi.")
                    return redirect('tambah_siswa')
                else:
                    messages.success(request, "Data berhasil disimpan.")
                    return redirect('data_siswa')
        else:
            form = AddSiswaForm()

        return render(request, 'data/siswa/tambah_siswa.html', {'form': form})
    else:
        return redirect('home')


@login_required
def edit_siswa(request, siswa_id):
    siswa = get_object_or_404(DataSiswa, pk=siswa_id)

    if request.user.is_superuser:
        if request.method == 'POST':
            form = EditSiswaForm(request.POST, instance=siswa)
            if form.is_valid():
                form.save()
                messages.success(request, 'Data siswa berhasil diperbarui.')
                return redirect('data_siswa')  # ganti ke url kamu
        else:
            form = EditSiswaForm(instance=siswa)

        return render(request, 'data/siswa/edit_siswa.html', {
            'form': form,
            'siswa': siswa
        })
    else:
        return redirect('home')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def hapus_siswa(request, siswa_id):
    siswa = get_object_or_404(DataSiswa, id=siswa_id)
    siswa.delete()
    messages.success(request, "Data siswa berhasil dihapus.")
    return redirect('data_siswa')  






@login_required
def data_guru(request):
    if request.user.is_superuser:
        query = request.GET.get('q', '')
        if query:
            data_guru = ProfileGuru.objects.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(nuptk__icontains=query) |
                Q(nomor_hp__icontains=query)
            )
        else:
            data_guru = ProfileGuru.objects.all()
        return render(request, 'data/guru/data_guru.html', {
            'data_guru': data_guru,
            'query': query,
        })
    else:
        return redirect('home')

@login_required
def detail_guru(request, pk):
    if request.user.is_superuser:
        guru = get_object_or_404(ProfileGuru, pk=pk)
        return render(request, 'data/guru/detail_guru.html', {'guru': guru})
    else:
        return redirect('home')

# Add Guru
@login_required
def tambah_guru(request):
    if request.user.is_superuser:

        if request.method == 'POST':
            form = AddGuruForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                form.save()

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
        
        return render(request, 'data/guru/tambah_guru.html', {'form': form})
    else:
        return redirect('home')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_guru(request, guru_id):
    profile_guru = get_object_or_404(ProfileGuru, id=guru_id)
    user = profile_guru.user

    if request.user.is_superuser:
        if request.method == 'POST':
            form = EditGuruForm(request.POST, instance=user)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()

                # Update data ProfileGuru
                profile_guru.nuptk = form.cleaned_data['nuptk']
                profile_guru.tempat_lahir = form.cleaned_data['tempat_lahir']
                profile_guru.tanggal_lahir = form.cleaned_data['tanggal_lahir']
                profile_guru.pendidikan_terakhir = form.cleaned_data['pendidikan_terakhir']
                profile_guru.nomor_hp = form.cleaned_data['nomor_hp']
                profile_guru.jabatan = form.cleaned_data['jabatan']
                profile_guru.tmt = form.cleaned_data['tmt']
                profile_guru.save()

                messages.success(request, 'Data guru berhasil diperbarui!')
                return redirect('data_guru')
        else:
            initial_data = {
                'nuptk': profile_guru.nuptk,
                'tempat_lahir': profile_guru.tempat_lahir,
                'tanggal_lahir': profile_guru.tanggal_lahir,
                'pendidikan_terakhir': profile_guru.pendidikan_terakhir,
                'nomor_hp': profile_guru.nomor_hp,
                'jabatan': profile_guru.jabatan,
                'tmt': profile_guru.tmt,
                'full_name': f"{user.first_name} {user.last_name}",
                'email': user.email,
                'username': user.username,
            }
            form = EditGuruForm(instance=user, initial=initial_data)

        return render(request, 'data/guru/edit_guru.html', {'form': form, 'profile_guru': profile_guru})
    else:
        return redirect('home')
    
@login_required
@user_passes_test(lambda u: u.is_superuser)
def hapus_guru(request, guru_id):
    guru = get_object_or_404(ProfileGuru, id=guru_id)
    user = guru.user  # Asumsi ada field OneToOneField ke User dengan nama 'user'
    user.delete()
    messages.success(request, "Data guru dan akun user berhasil dihapus.")
    return redirect('data_guru')  # ganti dengan nama URL ke daftar guru kamu





@login_required
def data_ortu(request):
    if request.user.is_superuser:
        query = request.GET.get('ortu', '')
        if query:
            data_ortu = OrangTuaMurid.objects.annotate(
                full_name=Concat('user__first_name', Value(' '), 'user__last_name')
            ).filter(
                Q(full_name__icontains=query) |
                Q(nomor_hp__icontains=query) |
                Q(siswa__nama_lengkap__icontains=query)
            )
        else:
            data_ortu = OrangTuaMurid.objects.all()

        return render(request, 'data/ortu/data_ortu.html', {
            'data_ortu': data_ortu,
            'query': query,
        })
    else:
        return redirect('home')


@login_required
def daftar_kelas(request):
    if request.user.is_superuser:
        # Ambil semua kelas dari database
        daftar_kelas = Kelas.objects.all()
        return render(request, 'data/kelas/daftar_kelas.html', {
            'daftar_kelas': daftar_kelas,
        })
    else:
        return redirect('home')



def edit_wali_kelas(request, kelas_id):
    if request.user.is_superuser:
        kelas = get_object_or_404(Kelas, id=kelas_id)
        if request.method == 'POST':
            form = EditWaliKelasForm(request.POST, instance=kelas)
            if form.is_valid():
                form.save()
                return redirect('daftar_kelas')  # ganti dengan nama url kamu
        else:
            form = EditWaliKelasForm(instance=kelas)
        return render(request, 'data/kelas/atur_wali_kelas.html', {'form': form, 'kelas': kelas})
    else:
        return redirect('home')
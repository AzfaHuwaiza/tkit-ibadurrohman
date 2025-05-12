from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from tkit.forms import *
from tkit.models import *

# Profile Orang Tua / Guru
@login_required
def my_profile(request):
    if request.user.is_superuser:
        return redirect('home')
    elif request.user.is_staff:
        # Profile Guru
        try:
            guru = ProfileGuru.objects.get(user=request.user)
        except ProfileGuru.DoesNotExist:
            guru = None

        context = {
            'full_name': request.user.get_full_name(),
            'username': request.user.username,
            'email': request.user.email,
            'nuptk': guru.nuptk if guru else '-',
            'tempat_lahir': guru.tempat_lahir if guru else '-',
            'tanggal_lahir': guru.tanggal_lahir if guru else '-',
            'pendidikan_terakhir': guru.pendidikan_terakhir if guru else '-',
            'nomor_hp': guru.nomor_hp if guru else '-',
            'jabatan': guru.jabatan if guru else '-',
            'tmt': guru.tmt if guru else '-',
        }

        return render(request, 'profiles/guru_profiles.html', context)
    else:
        # Profile Orang Tua
        try:
            ortu = OrangTuaMurid.objects.get(user=request.user)
        except OrangTuaMurid.DoesNotExist:
            ortu = None

        context = {
            'full_name': request.user.get_full_name(),
            'username': request.user.username,
            'email': request.user.email,
            'nomor_hp': ortu.nomor_hp if ortu else '-',
            'alamat': ortu.alamat if ortu else '-',
            'siswa': ortu.siswa if ortu else '-',
        }

        return render(request, 'profiles/ortu_profiles.html', context)
    
# Edit Profile Orang Tua
@login_required
def edit_profile_ortu(request):
    try:
        ortu = OrangTuaMurid.objects.get(user=request.user)
    except OrangTuaMurid.DoesNotExist:
        return redirect('home')  
    
    if request.method == 'POST':
        form_ortu = EditOrtuProfileForm(request.POST, instance=ortu)
        form_user = EditUserForm(request.POST, instance=request.user)
        if form_ortu.is_valid() and form_user.is_valid():
            form_user.save()
            form_ortu.save()
            return redirect('my_profile')
    else:
        form_ortu = EditOrtuProfileForm(instance=ortu)
        form_user = EditUserForm(instance=request.user)

    return render(request, 'profiles/edit_ortu_profile.html', {
        'form_ortu': form_ortu,
        'form_user': form_user
    })
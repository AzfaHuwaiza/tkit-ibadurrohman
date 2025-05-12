from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from collections import defaultdict, Counter 
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from django.utils.timezone import localdate
from tkit.forms import *
from tkit.utils import generate_periode_mingguan
from tkit.models import *
import datetime
import calendar
from datetime import date, datetime, timedelta
from django.http import HttpResponse


@login_required
def tambah_pengumuman(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = PengumumanForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('pengumuman') 
        else:
            form = PengumumanForm()
        
        return render(request, 'akademik/pengumuman/tambah_pengumuman.html', {'form': form})
    else:
        return redirect('home')

def pengumuman(request):
    pengumuman_list = Pengumuman.objects.order_by('-created_at')
    return render(request, 'akademik/pengumuman/pengumuman.html', {
        'pengumuman_list': pengumuman_list
    })

def detail_pengumuman(request, id):
    detail_pengumuman = get_object_or_404(Pengumuman, id=id)
    pengumuman_list = Pengumuman.objects.order_by('-created_at')
    
    url_pengumuman = request.build_absolute_uri()

    return render(request, 'akademik/pengumuman/detail_pengumuman.html', {
        'detail_pengumuman': detail_pengumuman,
        'pengumuman_list': pengumuman_list,
        'url_pengumuman': url_pengumuman,
    })




def pilih_kelas_perkembangan(request):
    if request.user.is_staff:
        kelas_list = Kelas.objects.filter(wali_kelas=request.user).order_by('nama_kelas')
        return render(request, 'akademik/perkembangan_anak/pilih_kelas.html', {
            'kelas_list': kelas_list
        })
    else:
        # Bagian untuk orang tua
        ortu = request.user
        data_ortu = get_object_or_404(OrangTuaMurid, user=ortu)
        siswa = data_ortu.siswa  # siswa yang diambil dari orang tua yang sedang login

        periode_list = Periode.objects.order_by('-tanggal_mulai')
        periode_id = request.GET.get('periode')
        if periode_id:
            periode = get_object_or_404(Periode, id=periode_id)
        else:
            periode = periode_list.first()

        # Filter perkembangan hanya untuk periode yang dipilih
        perkembangan_queryset = PerkembanganSiswa.objects.filter(
            siswa=siswa,
            periode=periode
        ).order_by('kategori')

        # Kelompokkan berdasarkan kategori
        perkembangan_by_kategori = defaultdict(list)
        for p in perkembangan_queryset:
            perkembangan_by_kategori[p.kategori].append(p)

        return render(request, 'akademik/perkembangan_anak/perkembangan_ortu.html', {
            'siswa': siswa,
            'periode_list': periode_list,
            'periode': periode,
            'perkembangan_by_kategori': dict(perkembangan_by_kategori),
            'tahun_ajaran': '2023/2024',
        })

@login_required
def rekap_perkelas(request, kelas_id):
    if request.user.is_staff:
        generate_periode_mingguan()
        kelas = get_object_or_404(Kelas, id=kelas_id)
        siswa = DataSiswa.objects.filter(kelas=kelas)

        periode_list = Periode.objects.order_by('-tanggal_mulai')
        periode_id = request.GET.get('periode')
        if periode_id:
            periode = get_object_or_404(Periode, id=periode_id)
        else:
            periode = periode_list.first()

        total = siswa.count()
        sudah = PerkembanganSiswa.objects.filter(siswa__in=siswa, periode=periode).values('siswa').distinct().count()
        belum = total - sudah

        rekap = PerkembanganSiswa.objects.filter(siswa__in=siswa, periode=periode)

        return render(request, 'akademik/perkembangan_anak/perkembangan_perkelas.html', {
            'kelas': kelas,
            'periode': periode,
            'periode_list': periode_list,
            'total': total,
            'sudah': sudah,
            'belum': belum,
            'rekap': rekap,
        })

KATEGORI_LIST = ["Kognitif", "Motorik", "Bahasa", "Sosial-Emosional", "Agama & Moral"]

@login_required
def input_perkembangan(request, kelas_id):
    periode_aktif = Periode.objects.order_by('-tanggal_mulai').first()
    siswa_kelas = DataSiswa.objects.filter(kelas_id=kelas_id).order_by('nama_lengkap')
    periode_aktif = Periode.objects.order_by('-tanggal_mulai').first()

    siswa_list = []
    kategori_per_siswa = {}

    for siswa in siswa_kelas:
        kategori_sudah = PerkembanganSiswa.objects.filter(
            siswa=siswa,
            periode=periode_aktif
        ).values_list('kategori', flat=True)

        kategori_belum = [k for k in KATEGORI_LIST if k not in kategori_sudah]

        if kategori_belum:
            siswa_list.append(siswa)
            kategori_per_siswa[siswa.id] = kategori_belum

    periode_list = Periode.objects.order_by('-tanggal_mulai')

    if request.method == 'POST':
        siswa_id = request.POST.get('siswa')
        kategori = request.POST.get('kategori')
        deskripsi = request.POST.get('deskripsi')
        catatan = request.POST.get('catatan')
        periode_id = request.POST.get('periode')

        PerkembanganSiswa.objects.create(
            siswa_id=siswa_id,
            kategori=kategori,
            deskripsi=deskripsi,
            catatan=catatan,
            periode_id=periode_id,
            guru=request.user  # << inilah yang penting
        )
        return redirect('rekap_perkelas', kelas_id=kelas_id)

    return render(request, 'akademik/perkembangan_anak/input_perkembangan.html', {
        'siswa_list': siswa_list,
        'kategori_per_siswa': kategori_per_siswa,
        'periode_list': periode_list,
        'periode_aktif': periode_aktif,
    })


def generate_calendar(year, month, absensi_qs):
    # Minggu sebagai hari pertama (6 = Sunday)
    cal = calendar.Calendar(firstweekday=6)
    days = []

    absensi_by_day = {
        ab.tanggal.day: ab.status
        for ab in absensi_qs
        if ab.tanggal.month == month and ab.tanggal.year == year
    }

    for week in cal.monthdayscalendar(year, month):
        for day in week:
            status = absensi_by_day.get(day, '') if day != 0 else ''
            days.append({
                'day': day,
                'status': status
            })

    return days
    cal = calendar.Calendar()
    days = []

    absensi_by_day = {
        ab.tanggal.day: ab.status
        for ab in absensi_qs
        if ab.tanggal.month == month and ab.tanggal.year == year
    }

    for week in cal.monthdayscalendar(year, month):
        for day in week:
            status = absensi_by_day.get(day, '') if day != 0 else ''
            days.append({
                'day': day,
                'status': status
            })

    return days
    cal = calendar.Calendar()
    days = []

    absensi_by_day = {
        ab.tanggal.day: ab.status
        for ab in absensi_qs
        if ab.tanggal.month == month and ab.tanggal.year == year
    }

    for week in cal.monthdayscalendar(year, month):
        for day in week:
            status = absensi_by_day.get(day, '') if day != 0 else ''
            days.append({
                'day': day,
                'status': status
            })

    return days

def menu_absensi(request):
    if request.user.is_staff:
        return render(request, 'akademik/absensi/menu_absensi.html')
    else:
        try:
            ortu = OrangTuaMurid.objects.get(user=request.user)
            siswa = ortu.siswa

            selected_bulan = request.GET.get('bulan', '')
            selected_status = request.GET.get('status', '')

            # Ambil tahun & bulan
            if selected_bulan:
                try:
                    tahun, bulan = map(int, selected_bulan.split('-'))
                except ValueError:
                    tahun, bulan = timezone.now().year, timezone.now().month
            else:
                tahun, bulan = timezone.now().year, timezone.now().month

            # Filter absensi hanya berdasarkan bulan
            absensi_bulanan = Absensi.objects.filter(
                siswa=siswa,
                tanggal__year=tahun,
                tanggal__month=bulan
            )

            # Ini untuk tabel: bisa difilter berdasarkan status kalau dipilih
            absensi_list = absensi_bulanan
            if selected_status and selected_status != 'Semua':
                absensi_list = absensi_list.filter(status=selected_status)

            # Rekap berdasarkan semua status di bulan itu (tanpa filter status)
            status_counter = Counter(absensi_bulanan.values_list('status', flat=True))
            hadir_count = status_counter.get('Hadir', 0)
            izin_count = status_counter.get('Izin', 0)
            sakit_count = status_counter.get('Sakit', 0)
            alfa_count = status_counter.get('Alfa', 0)

            # Informasi wali kelas
            kelas = siswa.kelas if siswa else None
            wali_kelas = None
            if kelas and kelas.wali_kelas:
                try:
                    wali_kelas = ProfileGuru.objects.get(user=kelas.wali_kelas)
                except ProfileGuru.DoesNotExist:
                    wali_kelas = None

            # Bulan list dinamis
            semua_absensi = Absensi.objects.filter(siswa=siswa)
            bulan_set = set((tgl.year, tgl.month) for tgl in semua_absensi.values_list('tanggal', flat=True))
            bulan_list = sorted(bulan_set, reverse=True)
            formatted_bulan_list = [
                (f"{tahun}-{bulan:02d}", f"{calendar.month_name[bulan]} {tahun}")
                for (tahun, bulan) in bulan_list
            ]

            # Generate kalender
            calendar_days = generate_calendar(tahun, bulan, absensi_bulanan)
            month_name = calendar.month_name[bulan]

        except OrangTuaMurid.DoesNotExist:
            ortu = None
            siswa = None
            absensi_list = []
            formatted_bulan_list = []
            selected_bulan = ''
            selected_status = ''
            hadir_count = izin_count = sakit_count = alfa_count = 0
            wali_kelas = None
            kelas = None
            calendar_days = []
            month_name = ''
            tahun = timezone.now().year

        context = {
            'absensi_list': absensi_list,
            'ortu': ortu,
            'bulan_list': formatted_bulan_list,
            'selected_bulan': selected_bulan,
            'selected_status': selected_status,
            'hadir_count': hadir_count,
            'izin_count': izin_count,
            'sakit_count': sakit_count,
            'alfa_count': alfa_count,
            'wali_kelas': wali_kelas,
            'kelas': kelas,
            'calendar_days': calendar_days,
            'month_name': month_name,
            'year': tahun,
        }

        return render(request, 'akademik/absensi/rekap_ortu.html', context)




@login_required
# def rekap_absen_Ortu(request):
def rekap_absensi(request):
    kelas_list = Kelas.objects.all()

    kelas_filter = request.GET.get('kelas', None)
    bulan_filter = request.GET.get('bulan', None)  # format dari input: 'YYYY-MM'
    today = date.today()

    # Parsing bulan dan tahun
    tahun = bulan = None
    if bulan_filter:
        try:
            tahun, bulan = map(int, bulan_filter.split('-'))
        except ValueError:
            bulan_filter = None  # invalid format

    # Ambil data absensi
    absensi_qs = Absensi.objects.all()

    # Filter berdasarkan kelas
    if kelas_filter:
        absensi_qs = absensi_qs.filter(siswa__kelas__nama_kelas=kelas_filter)

    # Filter berdasarkan bulan
    if bulan and tahun:
        try:
            tanggal_start = date(tahun, bulan, 1)
            next_month = tanggal_start.replace(day=28) + timedelta(days=4)

            tanggal_end = next_month.replace(day=1)
            absensi_qs = absensi_qs.filter(tanggal__gte=tanggal_start, tanggal__lt=tanggal_end)
        except ValueError:
            pass

    # Ambil siswa yang sesuai filter kelas
    siswa_list = DataSiswa.objects.filter(kelas__nama_kelas=kelas_filter) if kelas_filter else DataSiswa.objects.all()

    # Buat data rekap untuk setiap siswa
    data_rekap = []
    for siswa in siswa_list:
        absensi_siswa = absensi_qs.filter(siswa=siswa)

        total_hadir = absensi_siswa.filter(status='Hadir').count()
        total_izin = absensi_siswa.filter(status='Izin').count()
        total_sakit = absensi_siswa.filter(status='Sakit').count()
        total_alfa = absensi_siswa.filter(status='Alfa').count()
        total_hari = absensi_siswa.count()

        persen_kehadiran = (total_hadir / total_hari * 100) if total_hari > 0 else 0

        data_rekap.append({
            'siswa': siswa,
            'total_hadir': total_hadir,
            'total_izin': total_izin,
            'total_sakit': total_sakit,
            'total_alfa': total_alfa,
            'persen_kehadiran': round(persen_kehadiran, 2),
            'bulan_filter': bulan_filter,
            })

    # Statistik umum
    total_siswa = siswa_list.count()
    total_hadir = absensi_qs.filter(status='Hadir').count()
    total_absensi = absensi_qs.count()
    rata_rata_kehadiran = (total_hadir / total_absensi * 100) if total_absensi > 0 else 0
    total_ketidakhadiran = absensi_qs.exclude(status='Hadir').count()
    total_hari_efektif = absensi_qs.values('tanggal').distinct().count()

    context = {
        'kelas_list': kelas_list,
        'data_rekap': data_rekap,
        'total_siswa': total_siswa,
        'rata_rata_kehadiran': round(rata_rata_kehadiran, 2),
        'total_ketidakhadiran': total_ketidakhadiran,
        'total_hari_efektif': total_hari_efektif,
        'kelas_filter': kelas_filter,
        'bulan_filter': bulan_filter,
        'today': date.today(),
        
    }

    return render(request, 'akademik/absensi/rekap_absensi.html', context)

@login_required
def absensi(request):
    today = localdate()
    kelas_terpilih = None
    kelas_list = Kelas.objects.all()
    siswa_list = []

    if request.method == 'GET':
        kelas_id = request.GET.get('kelas')
        if kelas_id:
            try:
                kelas_terpilih = Kelas.objects.get(id=kelas_id)
                siswa_list = DataSiswa.objects.filter(kelas=kelas_terpilih)
            except Kelas.DoesNotExist:
                return HttpResponse("Kelas ID tidak valid.", status=400)

    elif request.method == 'POST':
        kelas_id = request.POST.get('kelas')
        if kelas_id:
            try:
                kelas_terpilih = Kelas.objects.get(id=kelas_id)
                siswa_list = DataSiswa.objects.filter(kelas=kelas_terpilih)
            except Kelas.DoesNotExist:
                return HttpResponse("Kelas ID tidak valid.", status=400)

            for siswa in siswa_list:
                status = request.POST.get(f'status_{siswa.id}')
                keterangan = request.POST.get(f'keterangan_{siswa.id}')

                absensi, created = Absensi.objects.get_or_create(
                    siswa=siswa,
                    tanggal=today
                )
                absensi.status = status
                absensi.keterangan = keterangan
                absensi.save()

            return redirect('halaman_berhasil')  # Ganti ini sesuai URL sukses kamu

    return render(request, 'akademik/absensi/absensi.html', {
        'today': today,
        'kelas_list': kelas_list,
        'kelas_terpilih': kelas_terpilih,
        'siswa_list': siswa_list,
    })
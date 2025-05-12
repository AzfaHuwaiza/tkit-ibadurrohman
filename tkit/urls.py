from django.urls import path
from .views import *
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls.static import static
from tkit.controller.auth import *
from tkit.controller.profile import *
from tkit.controller.data import *
from tkit.controller.akademik import *


urlpatterns = [
    path('', home_view, name='home'),

    # Authentication
    path('access/', pilih_akses, name='access'),  #All
    path('register/', register_ortu, name='register_ortu'), #All
    path('login-guru/', login_guru, name='login_guru'), #All
    path('login/', login_view, name='login'), #All
    path('logout/', logout_view, name='logout'), #All

    # Profile
    path('myprofile/', my_profile, name='my_profile'), #Guru. Ortu
    path('edit-profile/', edit_profile_ortu, name='edit_profile_ortu'), #Ortu

    # Menu
    path('menu/', pilih_menu, name='pilih_menu'), #All
    path('menu/data/', menu_data, name='menu_data'), #Admin


    # Data Kelas
    path('data/kelas/', daftar_kelas, name='daftar_kelas'), #Admin
    path('data/kelas/ubah/<int:kelas_id>/', edit_wali_kelas, name='edit_wali_kelas'), #Admin

    # Data Siswa
    path('data/siswa/', data_siswa, name='data_siswa'), #Admin, Guru
    path('data/siswa/tambah', tambah_siswa, name='tambah_siswa'), #Admin
    path('data/siswa/detail-<int:id>', detail_siswa, name='detail_siswa'), #Admin, Guru
    path('data/siswa/edit/<int:siswa_id>/', edit_siswa, name='edit_siswa'), #Admin
    path('data/siswa/hapus/<int:siswa_id>/', hapus_siswa, name='hapus_siswa'), #Admin

    # Data Guru
    path('data/guru/', data_guru, name='data_guru'), #Admin
    path('data/guru/tambah', tambah_guru, name='tambah_guru'), #Admin
    path('data/guru/detail-<int:pk>', detail_guru, name='detail_guru'), #Admin
    path('data/guru/edit/<int:guru_id>/', edit_guru, name='edit_guru'), #Admin
    path('data/guru/hapus/<int:guru_id>/', hapus_guru, name='hapus_guru'), #Admin

    # Kumpulan Data 
    path('data/orang-tua/', data_ortu, name='data_ortu'), #Admin

    # Pengumuman
    path('pengumuman/', pengumuman, name='pengumuman'), #All
    path('tambah-pengumuman/', tambah_pengumuman, name='tambah_pengumuman'), #Admin
    path('pengumuman/detail/<int:id>/', detail_pengumuman, name='detail_pengumuman'), #All

    # Perkembangan
    path('perkembangan/', pilih_kelas_perkembangan, name='pilih_kelas_perkembangan'), #Admin, Guru, Ortu= Langsung ke detail perkembangan
    path('perkembangan/<int:kelas_id>/', rekap_perkelas, name='rekap_perkelas'), #Admin, Guru
    path('perkembangan/kelas/<int:kelas_id>/input/', input_perkembangan, name='input_perkembangan'), #Admin, Guru
    
    # Absensi
    path('absensi/', menu_absensi, name='menu_absensi'), #Admin, Guru
    path('absensi/rekap/', rekap_absensi, name='rekap_absensi'), #Admin, Guru
    path('absensi/add/', absensi, name='absensi'), #Admin, Guru
    path('absensi/berhasil/', TemplateView.as_view(template_name='akademik/absensi/halaman_berhasil.html'), name='halaman_berhasil'),
    # path('absensi/ortu/', rekap_absensi_ortu, name='rekap_absensi_ortu'), #Admin, Guru

    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
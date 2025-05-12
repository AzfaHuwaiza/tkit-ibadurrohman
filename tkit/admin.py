from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from .models import OrangTuaMurid, ProfileGuru, DataSiswa, Pengumuman, Kelas, Periode, PerkembanganSiswa, Absensi

# Admin Profile Guru
class ProfileGuruStaff(admin.ModelAdmin):
    list_display = ('user', 'nuptk', 'tempat_lahir', 'tanggal_lahir', 'pendidikan_terakhir', 'nomor_hp', 'jabatan', 'tmt')
    search_fields = ('user__username', 'nuptk', 'nomor_hp')

# # Data Siswa
class ListDataSiswa(admin.ModelAdmin):
    list_display = ('nis', 'nisn', 'nama_lengkap','jenis_kelamin', 'tempat_lahir', 'tanggal_lahir', 'nama_orang_tua', 'alamat', 'no_hp_ortu', 'kelas')
    search_fields = ('nis', 'nisn', 'nama_lengkap', 'nama_orang_tua', 'no_hp_ortu', 'kelas__nama_kelas')

# Admin Profile Ortu
class ProfileOrtu(admin.ModelAdmin):
    list_display = ('user', 'nomor_hp', 'alamat', 'siswa')
    search_fields = ('user__username', 'alamat', 'nomor_hp', 'siswa__nama_lengkap')

class KelasAdminForm(forms.ModelForm):
    class Meta:
        model = Kelas
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mengatur queryset untuk hanya memilih User yang memiliki profileguru (yang berstatus guru)
        self.fields['wali_kelas'].queryset = User.objects.filter(profileguru__jabatan='Guru')  # Filter guru saja

class KelasAdmin(admin.ModelAdmin):
    form = KelasAdminForm
    list_display = ('nama_kelas', 'wali_kelas')

admin.site.register(ProfileGuru, ProfileGuruStaff)
admin.site.register(OrangTuaMurid, ProfileOrtu)
admin.site.register(DataSiswa, ListDataSiswa)
admin.site.register(Pengumuman)
admin.site.register(Kelas, KelasAdmin)
admin.site.register(Periode)
admin.site.register(PerkembanganSiswa)
admin.site.register(Absensi)
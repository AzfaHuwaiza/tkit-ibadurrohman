from django.db import models
from django.contrib.auth.models import User


# Model Profile Guru
class ProfileGuru(models.Model):
    JABATAN_CHOICES = [
        ('Guru', 'Guru'),
        ('Kepala Sekolah', 'Kepala Sekolah'),
        ('Staff', 'Staff'),
        ('Lainnya', 'Lainnya'),
    ]

    PENDIDIKAN_CHOICES = [
        ('Tamat SD/Sederajat', 'Tamat SD/Sederajat'),
        ('SLTP/Sederajat', 'SLTP/Sederajat'),
        ('SLTA/Sederajat', 'SLTA/Sederajat'),
        ('D3', 'D3'),
        ('D4', 'D4'),
        ('S1', 'S1'),
        ('S2', 'S2'),
        ('S3', 'S3'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=False)
    nuptk = models.CharField(max_length=16, null=True, blank=False, unique=True)
    tempat_lahir = models.CharField(max_length=255, null=True, blank=False)
    tanggal_lahir = models.DateField(null=True, blank=False)
    pendidikan_terakhir = models.CharField(
        max_length=20,
        choices=PENDIDIKAN_CHOICES,
        null=True,
        blank=False
    )
    nomor_hp = models.CharField(max_length=13, null=True, blank=False, unique=True)
    jabatan = models.CharField(
        max_length=20,
        choices=JABATAN_CHOICES,
        null=True,
        blank=False
    )
    tmt = models.DateField(null=True, blank=False)

    def __str__(self):
        return f"{self.user.username} - {self.jabatan if self.jabatan else 'Belum diatur'}"


# Model Kelas
class Kelas(models.Model):
    nama_kelas = models.CharField(max_length=100)
    wali_kelas = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nama_kelas

# Model Data Siswa
class DataSiswa(models.Model):
    nis = models.CharField(max_length=5, null=True, blank=False, unique=True)
    nisn = models.CharField(max_length=10, null=True, blank=False, unique=True)
    nama_lengkap = models.CharField(max_length=255, null=True, blank=False)
    jenis_kelamin = models.CharField(
        max_length=11,
        choices=[
            ('Laki-laki', 'Laki-laki'),
            ('Perempuan', 'Perempuan')
        ],
        null=True,
        blank=False
    )
    tempat_lahir = models.CharField(max_length=255, null=True, blank=False)
    tanggal_lahir = models.DateField(null=True, blank=False)
    nama_orang_tua = models.CharField(max_length=255, null=True, blank=False)
    alamat = models.CharField(max_length=255, null=True, blank=False)
    no_hp_ortu = models.CharField(max_length=14, null=True, blank=False, unique=True)
    kelas = models.ForeignKey(Kelas, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nama_lengkap or "Siswa Tanpa Nama"


# Model Profile Orang Tua
class OrangTuaMurid(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nomor_hp = models.CharField(max_length=15, unique=True, null=True, blank=True)
    alamat = models.CharField(max_length=255, null=True, blank=True)
    siswa = models.OneToOneField(DataSiswa, on_delete=models.SET_NULL, null=True, blank=True, related_name='ortu')

    def __str__(self):
        return self.user.username if self.user else 'Tidak Ada Pengguna'

# Model Pengumuman
class Pengumuman(models.Model):
    TIPE_CHOICES = [
        ('PPDB', 'PPDB'),
        ('Akademik', 'Akademik'),
        ('Libur', 'Libur'),
        ('Kegiatan', 'Kegiatan'),
        ('Keuangan', 'Keuangan'),
        ('Lainnya', 'Lainnya'),
    ]

    tipe = models.CharField(max_length=20, choices=TIPE_CHOICES)
    subjek = models.CharField(max_length=255)
    deskripsi = models.TextField()
    file_surat = models.FileField(upload_to='akademik/surat_pengumuman/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipe} - {self.subjek}"

# Model Periode
class Periode(models.Model):
    minggu = models.CharField(max_length=50)  # e.g., "Minggu 1 - Maret 2024"
    tanggal_mulai = models.DateField()
    tanggal_selesai = models.DateField()

    def __str__(self):
        return self.minggu

# Model Perkembangan Siswa
class PerkembanganSiswa(models.Model):
    siswa = models.ForeignKey(DataSiswa, on_delete=models.CASCADE)
    guru = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    periode = models.ForeignKey(Periode, on_delete=models.SET_NULL, null=True)
    kategori = models.CharField(max_length=50, choices=[
        ('Kognitif', 'Kognitif'),
        ('Motorik', 'Motorik'),
        ('Bahasa', 'Bahasa'),
        ('Sosial-Emosional', 'Sosial-Emosional'),
        ('Agama & Moral', 'Agama & Moral'),
    ])
    deskripsi = models.TextField()
    catatan = models.TextField()
    tanggal_input = models.DateTimeField(auto_now_add=True)

class Absensi(models.Model):
    siswa = models.ForeignKey(DataSiswa, on_delete=models.CASCADE)
    tanggal = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('Hadir', 'Hadir'),
        ('Izin', 'Izin'),
        ('Sakit', 'Sakit'),
        ('Alfa', 'Alfa'),
    ])
    keterangan = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.siswa.nama_lengkap} - {self.tanggal} - {self.status}"
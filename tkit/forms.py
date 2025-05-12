from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *

User = get_user_model()


# FORM REGISTER ORTU
class CustomRegister_Ortu(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        help_text='Username dapat berisi karakter apa pun.',
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        }),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email',
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        }),
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nama Depan',
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        }),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nama Belakang',
            'class': 'mt-1 shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        }),
    )
    nisn_siswa = forms.CharField(
        max_length=16,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Masukkan NISN anak anda',
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        }),
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        }),
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Masukkan kembali Password',
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        }),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email ini sudah digunakan. Silakan gunakan email lain.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username ini sudah digunakan. Silakan pilih username lain.')
        return username

    def clean_nisn_siswa(self):
        nisn = self.cleaned_data.get('nisn_siswa')
        try:
            siswa = DataSiswa.objects.get(nisn=nisn)
        except DataSiswa.DoesNotExist:
            raise forms.ValidationError('NISN tidak ditemukan atau belum terdaftar.')

        if OrangTuaMurid.objects.filter(siswa=siswa).exists():
            raise forms.ValidationError('Siswa ini sudah memiliki akun orang tua.')

        return siswa

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user

# FORM LOGIN ORTU
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username, Email atau nomor HP',
        max_length=254,
        widget=forms.TextInput(attrs={
            'placeholder': 'Masukkan Username, Email, atau Nomor HP',
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        }),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Masukkan Password',
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        }),
    )

# FORM EDIT USER
class EditUserForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email',
            'class' : "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            }),
    )

    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nama Depan',
            'class' : "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            }),
    )

    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nama Belakang',
            'class' : "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            }),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


# FORM ADD GURU
class AddGuruForm(forms.ModelForm):
    full_name = forms.CharField(
        label='Nama Lengkap',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nama Lengkap Guru',
            'class': "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        }),
    )

    nuptk = forms.CharField(
        label='NUPTK',
        max_length=16,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'NUPTK Guru',
            'class': "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        }),
    )

    tempat_lahir = forms.CharField(
        label='Tempat Lahir',
        max_length=225,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Tempat Lahir Guru',
            'class': "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        }),
    )

    tanggal_lahir = forms.DateField(
        label='Tanggal Lahir',
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        }),
    )

    pendidikan_terakhir = forms.ChoiceField(
        label='Pendidikan Terakhir',
        choices=[('', '----------')] + list(ProfileGuru.PENDIDIKAN_CHOICES),
        required=True,
                error_messages={
            'required': 'Silakan pilih pendidikan terakhir.'
        },
        widget=forms.Select(attrs={
            'class': "mt-1 shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        }),
    )

    jabatan = forms.ChoiceField(
        label='Jabatan',
        choices=[('', '----------')] + list(ProfileGuru.JABATAN_CHOICES),
        required=True,
        error_messages={
            'required': 'Silakan pilih jabatan.'
        },
        widget=forms.Select(attrs={
            'class': "mt-1 shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        }),
    )

    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email Aktif Guru',
            'class': "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        }),
    )

    nomor_hp = forms.CharField(
        label='Nomor HP',
        max_length=13,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nomor HP Aktif Guru',
            'class': "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        }),
    )

    tmt = forms.DateField(
        label='TMT',
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        }),
    )

    username = forms.CharField(
        label='Username',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username Baru Guru',
            'class': "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        }),
    )

    password = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password Baru Guru',
            'class': "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        }),
    )

    def clean_nomor_hp(self):
        no_hp = self.cleaned_data.get('nomor_hp')
        if no_hp.startswith('0'):
            no_hp = '62' + no_hp[1:]
        return no_hp

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True  # Tandai sebagai staff (guru)

        full_name = self.cleaned_data['full_name']
        name_parts = full_name.strip().split(' ', 1)
        user.first_name = name_parts[0]
        user.last_name = name_parts[1] if len(name_parts) > 1 else ''

        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = [
            'nuptk', 'full_name', 'tempat_lahir', 'tanggal_lahir',
            'nomor_hp', 'tmt', 'email', 'username', 'password'
        ]

# FORM EDIT GURU
class EditGuruForm(forms.ModelForm):
    full_name = forms.CharField(
        label='Nama Lengkap',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nama Lengkap Guru',
            'class': "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        }),
    )

    nuptk = forms.CharField(
        label='NUPTK',
        max_length=16,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'NUPTK Guru',
            'class': "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        }),
    )

    tempat_lahir = forms.CharField(
        label='Tempat Lahir',
        max_length=225,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Tempat Lahir Guru',
            'class': "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        }),
    )

    tanggal_lahir = forms.DateField(
        label='Tanggal Lahir',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        }, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d'],
    )

    pendidikan_terakhir = forms.ChoiceField(
        label='Pendidikan Terakhir',
        choices=ProfileGuru.PENDIDIKAN_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        }),
    )

    jabatan = forms.ChoiceField(
        label='Jabatan',
        choices=ProfileGuru.JABATAN_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        }),
    )

    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email Aktif Guru',
            'class': "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        }),
    )

    nomor_hp = forms.CharField(
        label='Nomor HP',
        max_length=13,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nomor HP Aktif Guru',
            'class': "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        }),
    )

    tmt = forms.DateField(
        label='TMT',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        }, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d'],
    )

    username = forms.CharField(
        label='Username',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username Baru Guru',
            'class': "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        }),
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_nomor_hp(self):
        no_hp = self.cleaned_data.get('nomor_hp')
        if no_hp and no_hp.startswith('0'):
            no_hp = '62' + no_hp[1:]
        return no_hp

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True

        full_name = self.cleaned_data['full_name']
        parts = full_name.strip().split(' ', 1)
        user.first_name = parts[0]
        user.last_name = parts[1] if len(parts) > 1 else ''

        if commit:
            user.save()
        return user

# FORM ADD SISWA
class AddSiswaForm(forms.ModelForm):
    nis = forms.CharField(
        label='NIS',
        min_length=5,
        max_length=5,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    
    nisn = forms.CharField(
        label='NISN',
        min_length=10,
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    
    nama_lengkap = forms.CharField(
        label='Nama Lengkap',
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nama Lengkap Siswa',
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    
    tempat_lahir = forms.CharField(
        label='Tempat Lahir',
        max_length=225,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Tempat Lahir Siswa',
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    
    nama_orang_tua = forms.CharField(
        label='Nama Orang Tua',
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nama Orang Tua Siswa',
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    
    alamat = forms.CharField(
        label='Alamat',
        max_length=500,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Alamat Siswa',
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    
    no_hp_ortu = forms.CharField(
        label='Nomor HP Orang Tua',
        max_length=13,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nomor HP Orang Tua',
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    
    tanggal_lahir = forms.DateField(
        label='Tanggal Lahir',
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    
    jenis_kelamin = forms.ChoiceField(
        label='Jenis Kelamin',
        required=True,
        choices=[('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')],
        widget=forms.Select(attrs={
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    
    kelas = forms.ModelChoiceField(
        queryset=Kelas.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )

    class Meta:
        model = DataSiswa
        fields = '__all__'

# FORM ADD SISWA
class EditSiswaForm(forms.ModelForm):
    nis = forms.CharField(
        label='NIS',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Masukkan NIS',
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    
    nisn = forms.CharField(
        label='NISN',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Masukkan NISN',
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    
    nama_lengkap = forms.CharField(
        label='Nama Lengkap',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nama Lengkap Siswa',
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    
    tempat_lahir = forms.CharField(
        label='Tempat Lahir',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Tempat Lahir Siswa',
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    
    tanggal_lahir = forms.DateField(
        label='Tanggal Lahir',
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        }, format='%Y-%m-%d'
        )
    )
    
    nama_orang_tua = forms.CharField(
        label='Nama Orang Tua',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nama Orang Tua Siswa',
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    
    alamat = forms.CharField(
        label='Alamat',
        max_length=500,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Alamat Siswa',
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )
    
    no_hp_ortu = forms.CharField(
        label='Nomor HP Orang Tua',
        max_length=13,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nomor HP Orang Tua',
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )

    kelas = forms.ModelChoiceField(
        queryset=Kelas.objects.all(),
        label='Kelas',
        required=True,
        widget=forms.Select(attrs={
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )

    JENIS_KELAMIN_CHOICES = [
        ('Laki-laki', 'Laki-laki'),
        ('Perempuan', 'Perempuan'),
    ]

    jenis_kelamin = forms.ChoiceField(
        label='Jenis Kelamin',  
        required=True,
        choices=JENIS_KELAMIN_CHOICES,
        widget=forms.Select(attrs={
            'class': 'shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 '
        })
    )

    class Meta:
        model = DataSiswa
        fields = '__all__'

# FORM EDIT GURU
class EditOrtuProfileForm(forms.ModelForm):
    nomor_hp = forms.CharField(
        label='Nomor HP Aktif',
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nomor HP Aktif',
            'class': "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        })
    )

    alamat = forms.CharField(
        label='Alamat Rumah',
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Alamat Rumah',
            'class': "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        })
    )

    class Meta:
        model = OrangTuaMurid
        fields = ['nomor_hp', 'alamat']


# FORM INPUT PENGUMUMAN
class PengumumanForm(forms.ModelForm):
    subjek = forms.CharField(
        label='Subjek',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Masukkan subjek Pengumuman',
            'class': 'mt-1 shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )

    deskripsi = forms.CharField(
        label='Deskripsi',
        required=True,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Masukkan deskripsi Pengumuman',
            'class': 'mt-1 shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
    )

    file_surat = forms.FileField(
        label='File Surat',
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'accept': '.pdf,.doc,.docx',
            'class': 'mt-1 shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        }),
        help_text='PDF, DOC, atau DOCX hingga 10MB'
    )



    class Meta:
        model = Pengumuman
        fields = ['tipe', 'subjek', 'deskripsi', 'file_surat']
        widgets = {
            'tipe': forms.Select(attrs={
                'class': 'mt-1 shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            })
        }

    def clean_file_surat(self):
        file = self.cleaned_data.get('file_surat', False)
        if file:
            # Cek ukuran file (10MB = 10*1024*1024 bytes)
            if file.size > 10 * 1024 * 1024:
                raise ValidationError("Ukuran file maksimal 10MB.")

            # Cek ekstensi file
            valid_extensions = ['.pdf', '.doc', '.docx']
            import os
            ext = os.path.splitext(file.name)[1].lower()
            if ext not in valid_extensions:
                raise ValidationError("Format file harus PDF, DOC, atau DOCX.")
        
        return file

class AssignKelasForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kelas = kwargs.pop('kelas', None)
        super().__init__(*args, **kwargs)

        if kelas:
            # Hanya siswa yang belum punya kelas atau sudah di kelas yang dipilih
            queryset = DataSiswa.objects.filter(models.Q(kelas__isnull=True) | models.Q(kelas=kelas))
        else:
            queryset = DataSiswa.objects.none()  # jangan munculin apa-apa kalau belum pilih kelas

        self.fields['siswa'] = forms.ModelMultipleChoiceField(
            queryset=queryset,
            label="Pilih Siswa",
            widget=forms.CheckboxSelectMultiple,
            required=False
        )
        if kelas:
            self.fields['siswa'].initial = queryset.filter(kelas=kelas)

class EditWaliKelasForm(forms.ModelForm):
    wali_kelas = forms.ModelChoiceField(
        queryset=User.objects.filter(profileguru__isnull=False),  # Ambil User yang memiliki ProfileGuru
        label='Wali Kelas',
        required=True,
        widget=forms.Select(attrs={
            'class': "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        })
    )

    class Meta:
        model = Kelas
        fields = ['wali_kelas']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mengatur queryset untuk hanya memilih User yang memiliki profileguru (yang berstatus guru)
        self.fields['wali_kelas'].queryset = User.objects.filter(profileguru__jabatan='Guru')  # Filter guru saja



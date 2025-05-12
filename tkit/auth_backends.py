from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from tkit.models import OrangTuaMurid  # pastiin ini sesuai path kamu

User = get_user_model()

class EmailOrUsernameOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Coba cari user berdasarkan username atau email
            user = User.objects.filter(Q(username=username) | Q(email=username)).first()

            # Kalau belum ketemu, cari berdasarkan nomor HP di model OrangTuaMurid
            if not user:
                ortu_profile = OrangTuaMurid.objects.filter(nomor_hp=username).first()
                if ortu_profile:
                    user = ortu_profile.user
        except User.DoesNotExist:
            return None

        if user and user.check_password(password):
            return user
        return None

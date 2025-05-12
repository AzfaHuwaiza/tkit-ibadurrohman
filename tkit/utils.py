from datetime import date, timedelta
from .models import Periode

# Generate Otomatis Periode Perkembangan Mingguan
def generate_periode_mingguan():
    today = date.today()

    existing = Periode.objects.filter(tanggal_mulai__lte=today, tanggal_selesai__gte=today).first()

    if not existing:
        start_of_week = today - timedelta(days=today.weekday())  # Senin
        end_of_week = start_of_week + timedelta(days=6)  # Minggu

        minggu_str = f"{start_of_week.strftime('%d %b')} - {end_of_week.strftime('%d %b %Y')}"

        Periode.objects.create(
            minggu=minggu_str,
            tanggal_mulai=start_of_week,
            tanggal_selesai=end_of_week
        )

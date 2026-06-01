from datetime import datetime
import pytz

def format_waktu_ke_wib(waktu_utc_string):
    # 1. Ubah string dari API (misal: "2026-06-01T09:31:00") menjadi objek datetime
    # Jika API mengirimkan akhiran 'Z', ganti dengan format yang dikenali
    if waktu_utc_string.endswith("Z"):
        waktu_utc_string = waktu_utc_string[:-1]
        
    waktu_obj = datetime.fromisoformat(waktu_utc_string)
    
    # 2. Beritahu Python bahwa waktu ini adalah UTC
    if waktu_obj.tzinfo is None:
        waktu_obj = waktu_obj.replace(tzinfo=pytz.UTC)
        
    # 3. Konversi ke zona waktu Asia/Jakarta (WIB)
    wib_tz = pytz.timezone("Asia/Jakarta")
    waktu_wib = waktu_obj.astimezone(wib_tz)
    
    # 4. Format kembali menjadi string yang cantik
    return waktu_wib.strftime("%d %b %Y, %H:%M WIB")
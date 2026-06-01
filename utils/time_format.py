from datetime import datetime
from zoneinfo import ZoneInfo

def format_waktu_ke_wib(waktu_utc_string):
    # 1. Parsing string (FastAPI biasanya mengirim format ISO 8601)
    if waktu_utc_string.endswith("Z"):
        waktu_utc_string = waktu_utc_string[:-1]
        
    waktu_obj = datetime.fromisoformat(waktu_utc_string)
    
    # 2. Tetapkan sebagai UTC
    if waktu_obj.tzinfo is None:
        waktu_obj = waktu_obj.replace(tzinfo=ZoneInfo("UTC"))
        
    # 3. Konversi ke Waktu Indonesia Barat (WIB)
    waktu_wib = waktu_obj.astimezone(ZoneInfo("Asia/Jakarta"))
    
    return waktu_wib.strftime("%d %b %Y, %H:%M WIB")
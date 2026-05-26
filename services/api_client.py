import os
import streamlit as st
import requests
import time
from session.auth_state import logout_user

api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")

def _get_headers(token: str):
    """
    helper untuk membuat header http.
    wajib menggunakan jwt valid untuk semua request terproteksi.
    """
    if not token:
        raise ValueError("token autentikasi tidak valid atau kosong.")
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

# --- python decorator: otomatis me-logout user saat JWT kadaluarsa (error 401) ---
def handle_auth_errors(func):
    """
    Decorator untuk mencegat error 401 dari backend
    dan melakukan auto-logout secara elegan.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 401:
                st.toast("⚠️ Sesi Anda telah berakhir. Mengalihkan ke halaman login...", icon="🔒")
                time.sleep(1.5) # Beri waktu agar pesan toast terbaca
                
                logout_user() # fungsi pembersih token
                st.switch_page("pages/02_login.py")
                st.stop() # hentikan rendering halaman saat ini
            
            # Jika error lain (misal 500 atau 404), biarkan errornya lewat
            raise e
    return wrapper

# --- modul auth ---
@handle_auth_errors
def login(email, password):
    """
    mengirim kredensial login ke fastapi (biasanya format form-data untuk oauth2).
    """
    url = f"{api_base_url}/auth/login"
    # fastapi oauth2passwordrequestform mengharuskan 'username' dan 'password' dalam form data
    data = {"username": email, "password": password}
    
    response = requests.post(url, data=data, timeout=10)
    response.raise_for_status()
    return response.json()

@handle_auth_errors
def register(nama, email, password, age=None, skin_type=None):
    """
    mendaftarkan user baru dengan mengirimkan payload lengkap ke FastAPI.
    """
    url = f"{api_base_url}/auth/register"
    payload = {
        "nama": nama, 
        "email": email, 
        "password": password,
        "age": age,            # Menggunakan penamaan skema backend
        "skin_type": skin_type   # Menggunakan penamaan skema backend
    }
    
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()

# --- modul prediksi & media ---
@handle_auth_errors
def upload_image_for_prediction(file_bytes, filename, token, extra_data="{}"):
    """
    mengirim gambar ke backend untuk diproses.
    """
    url = f"{api_base_url}/predictions/predict"
    files = {"file": (filename, file_bytes, "image/jpeg")}

    # data payload untuk Form() di FastAPI
    payload = {"extra_data": extra_data}
    
    response = requests.post(url, headers=_get_headers(token), files=files, timeout=15)
    
    # cegat error validasi wajah
    if response.status_code == 400:
        # ambil pesan asli dari OpenCV di backend
        error_data = response.json()
        error_msg = error_data.get("detail", "Gambar ditolak. Silakan unggah foto wajah yang jelas.")
        
        # Tampilkan peringatan kuning di Streamlit
        st.warning(f"⚠️ {error_msg}")
        
        # Hentikan eksekusi kode sepenuhnya agar Streamlit tidak lanjut menggambar progress bar
        st.stop()
    
    # Jika error lain (misal 500), lemparkan seperti biasa
    response.raise_for_status()
    return response.json()

@handle_auth_errors
def get_prediction(job_id, token):
    """
    mengambil status dan hasil prediksi menggunakan single endpoint konsisten.
    schema respons yang diharapkan:
    { "job_id": "...", "status": "...", "result": {...}, "error": "..." }
    """
    url = f"{api_base_url}/predictions/{job_id}"
    
    response = requests.get(url, headers=_get_headers(token), timeout=5)
    response.raise_for_status()
    return response.json()

# --- modul user & riwayat ---
@handle_auth_errors
def get_user_history(token):
    """
    mengambil riwayat prediksi user dari postgresql via fastapi.
    """
    url = f"{api_base_url}/predictions/history"
    
    response = requests.get(url, headers=_get_headers(token), timeout=10)
    response.raise_for_status()
    return response.json()

# --- modul user & profile ---
def get_current_user(token: str) -> dict:
    url = f"{api_base_url}/users/me"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code}: {response.text}")
    return response.json()

def update_user_profile(token: str, payload: dict) -> dict:
    url = f"{api_base_url}/users/me"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code}: {response.text}")
    return response.json()

# --- fungsi fetching untuk billing ---
def get_billing_info(token: str) -> dict:
    """
    Mengambil info paket dan sisa kuota dari backend.
    """
    url = f"{api_base_url}/billing/me"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            # tampilkan error asli di UI untuk DEBUGGING
            st.error(f"API Billing Error {response.status_code}: {response.text}")
            return {"active_plan": f"Error {response.status_code}", "remaining_quota": 0}
    except Exception as e:
        st.error(f"Gagal koneksi ke API: {str(e)}")
        return {"active_plan": "Koneksi Terputus", "remaining_quota": 0}
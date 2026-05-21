import os
import streamlit as st
import requests

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

# --- modul auth ---
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

def upload_image_for_prediction(file_bytes, filename, token, extra_data="{}"):
    """
    mengirim gambar ke backend untuk diproses.
    """
    url = f"{api_base_url}/predictions/predict"
    files = {"file": (filename, file_bytes, "image/jpeg")}

    # data payload untuk Form() di FastAPI
    payload = {"extra_data": extra_data}
    
    response = requests.post(url, headers=_get_headers(token), files=files, timeout=15)
    response.raise_for_status()
    return response.json()

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
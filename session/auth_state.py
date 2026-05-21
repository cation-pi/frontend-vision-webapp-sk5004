import os
import time
import streamlit as st
from streamlit_cookies_controller import CookieController
from services.api_client import login, register, get_billing_info

cookie_controller = CookieController()

# feature flag khusus konfigurasi cloud
BILLING_ENABLED = st.secrets.get("BILLING_ENABLED", False)

def refresh_billing_state():
    """Memperbarui data kuota di session state jika fitur billing aktif."""
    if not BILLING_ENABLED:
        return
        
    token = st.session_state.get("access_token")
    if token and st.session_state.get("logged_in"):
        st.session_state.billing_info = get_billing_info(token)

def init_auth_state():
    """
    mengecek token di session state dan cookie saat aplikasi dimuat.
    """
    # pastikan state dasar ada saat baru di-refresh
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # jika token kosong di memori, cari di cookie
    if not st.session_state.get("access_token"):
        token_di_cookie = None
        try:
            token_di_cookie = cookie_controller.get("access_token")
        except TypeError:
            token_di_cookie = None
        
        if token_di_cookie:
            # sinkronkan semua state penting
            st.session_state["access_token"] = token_di_cookie
            st.session_state.logged_in = True  # <-- Menghilangkan error "Page not found"
            
            # berikan fallback user_info agar UI tidak crash saat memanggil nama profil
            if "user_info" not in st.session_state or not st.session_state.user_info:
                st.session_state.user_info = {"nama": "Pengguna", "email": ""}
            
            # billing state
            refresh_billing_state()

        else:
            st.session_state["access_token"] = None
            st.session_state.logged_in = False

def init_session_state():
    """
    menginisialisasi variabel state untuk autentikasi jika belum ada.
    """
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "access_token" not in st.session_state:
        st.session_state["access_token"] = None
    if "user_info" not in st.session_state:
        st.session_state.user_info = {}
    if "role" not in st.session_state:
        st.session_state.role = "user"

def authenticate_user(email, password):
    """
    menangani alur login: memanggil api, menyimpan token ke session state dan cookie.
    """
    try:
        data = login(email, password)
        token = data.get("access_token")
        
        # simpan jwt dan status login di memori Streamlit
        st.session_state["access_token"] = token
        st.session_state.logged_in = True
        
        # asumsikan backend mengembalikan info user saat login
        st.session_state.user_info = {
            "email": email,
            "nama": data.get("nama", "pengguna")
        }
        
        # tangkap role jika ada (untuk panel admin)
        st.session_state.role = data.get("role", "user")
        
        # cookie
        if token:
            cookie_controller.set("access_token", token)
        
        # billing state
        refresh_billing_state()

        return True, "berhasil login."
        
    except Exception as e:
        # bersihkan state jika gagal
        logout_user()
        return False, "Gagal login. Kredensial salah atau server gangguan."

def register_user(nama, email, password, age=None, skin_type=None):
    """
    menangani pendaftaran pengguna baru dengan metadata tambahan.
    """
    try:
        # Teruskan argumen age dan skin_type ke fungsi API client
        register(nama, email, password, age, skin_type)
        return True, "Registrasi berhasil. Silakan login."
    except Exception as e:
        return False, f"Registrasi gagal. Email mungkin sudah terdaftar."

def logout_user():
    """
    menghapus token aktif dari browser dan menyapu bersih state spesifik.
    """
    # 1. Timpa token dengan string kosong terlebih dahulu
    cookie_controller.set("access_token", "")
    time.sleep(0.1)
    
    # 2. Baru perintahkan browser untuk menghapusnya
    cookie_controller.remove("access_token")

    # 3. Hapus HANYA data aplikasi
    keys_to_delete = [
        "access_token", 
        "logged_in", 
        "user_info", 
        "role",
        "billing_info", 
        "profil", 
        "profil_fetched", 
        "history"
    ]
    
    for key in keys_to_delete:
        st.session_state.pop(key, None)

    # 4. Beri jeda akhir sebelum Streamlit melakukan rerun otomatis (jika ada st.rerun di app.py)
    time.sleep(0.5)
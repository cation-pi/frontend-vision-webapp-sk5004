import streamlit as st

def require_auth():
    """
    Fungsi untuk mengecek apakah user sudah login.
    Jika belum, arahkan kembali ke halaman login.
    """
    if "access_token" not in st.session_state or not st.session_state["access_token"]:
        st.warning("Akses ditolak. Silakan login terlebih dahulu.")
        st.stop() # Menghentikan eksekusi halaman di bawahnya

def get_current_user():
    """Mengambil data user yang sedang login dari session state."""
    if "user_data" in st.session_state:
        return st.session_state["user_data"]
    return None
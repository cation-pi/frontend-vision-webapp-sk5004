import streamlit as st
import time
import re
from session.auth_state import register_user

# ── Helper Validasi Email
def valid_email(email):
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email) is not None

# ── Proteksi Halaman (Jika sudah login)
if st.session_state.get("logged_in"):
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1a6ec8,#3a9bd5);border-radius:14px;
                padding:1.2rem 1.6rem;margin-bottom:1.2rem;">
        <h2 style="margin:0;color:white;">✅ Sudah Masuk</h2>
        <p style="margin:0.3rem 0 0;color:#d0eaff;font-size:0.9rem;">
            Kamu sudah login.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.info("Silakan navigasi ke halaman lain melalui sidebar.")
    st.stop()

# ── Header UI Acnelytics
st.markdown("""
<div style="background:linear-gradient(135deg,#1a6ec8,#3a9bd5);border-radius:14px;
            padding:1.4rem 1.6rem 1.2rem;margin-bottom:1.4rem;text-align:center;">
    <div style="font-size:2rem;margin-bottom:0.3rem;">📝</div>
    <h2 style="margin:0;color:white;font-size:1.4rem;">Buat Akun Baru</h2>
    <p style="margin:0.3rem 0 0;color:#d0eaff;font-size:0.88rem;">
        Isi data di bawah untuk membuat akun Acnelytics
    </p>
</div>
""", unsafe_allow_html=True)

# ── Form Registrasi
nama = st.text_input("Nama Lengkap", placeholder="contoh: Andi")

# Kolom agar UI lebih padat dan rapi
col1, col2 = st.columns(2)
with col1:
    usia = st.text_input("Usia", placeholder="contoh: 22")
with col2:
    pilihan_kulit = ["", "Normal", "Berminyak", "Kering", "Kombinasi", "Sensitif"]
    jenis_kulit = st.selectbox("Jenis Kulit (opsional)", options=pilihan_kulit)

email = st.text_input("Email", placeholder="contoh@email.com")
password = st.text_input("Password", type="password", placeholder="Minimal 6 karakter")
konfirmasi_password = st.text_input("Konfirmasi Password", type="password")

# ── Eksekusi API
if st.button("📝 Daftar Sekarang", use_container_width=True):
    # Validasi Kelengkapan di sisi frontend
    if not (nama and usia and email and password and konfirmasi_password):
        st.warning("Harap isi semua kolom form yang wajib (Nama, Usia, Email, Password).")
    elif not valid_email(email):
        st.warning("Format email tidak valid.")
    elif len(password) < 6:
        st.warning("Password minimal 6 karakter.")
    elif password != konfirmasi_password:
        st.warning("Password dan konfirmasi password tidak cocok. Silakan periksa kembali.")
    else:
        with st.spinner("Mengirim data ke server..."):
            # Konversi usia ke integer secara aman sebelum dikirim
            age_val = None
            try:
                if usia:
                    age_val = int(usia)
            except ValueError:
                pass
            
            skin_type_val = jenis_kulit if jenis_kulit else None
            
            # Oper parameter tambahan ke register_user
            success, msg = register_user(
                nama=nama, 
                email=email, 
                password=password, 
                age=age_val, 
                skin_type=skin_type_val
            )
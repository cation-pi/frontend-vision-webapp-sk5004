import streamlit as st
import time
from session.auth_state import authenticate_user

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
    <div style="font-size:2rem;margin-bottom:0.3rem;">🔑</div>
    <h2 style="margin:0;color:white;font-size:1.4rem;">Masuk</h2>
    <p style="margin:0.3rem 0 0;color:#d0eaff;font-size:0.88rem;">
        Masukkan email dan password kamu untuk melanjutkan
    </p>
</div>
""", unsafe_allow_html=True)

# ── Tangkap Sinyal CTA (Call to Action) dari Home
if st.query_params.get("cta") == "true":
    st.info("👋 Silakan login atau daftar akun terlebih dahulu untuk mulai analisis foto.")
    st.query_params.clear()

# ── Form Login
email = st.text_input("Email", placeholder="contoh@email.com")
password = st.text_input("Password", type="password")

if st.button("🔓 Masuk", use_container_width=True):
    if email and password:
        with st.spinner("Memverifikasi kredensial..."):
            success, msg = authenticate_user(email, password)
            
            if success:
                st.success("✅ Login berhasil!")
                time.sleep(1) 
                st.rerun() 
            else:
                st.error(msg)
    else:
        st.warning("Harap isi email dan password terlebih dahulu.")

# ── Navigasi ke Halaman Register
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<p style="text-align:center;font-size:0.88rem;color:#444;margin-top:0.5rem; margin-bottom:0.2rem;">
    Belum punya akun?
</p>
""", unsafe_allow_html=True)

# Menggunakan column agar tombol berada di tengah (opsional, tapi lebih rapi)
_, col_btn, _ = st.columns([1, 2, 1])
with col_btn:
    if st.button("📝 Daftar Sekarang", use_container_width=True):
        st.switch_page("pages/03_register.py")
import streamlit as st
import time
from session.auth_state import authenticate_user

st.title("login (placeholder)")
st.write("halaman ini digunakan sebagai referensi alur API. nanti bisa diganti UInya.")

# tangkap sinyal dari tombol "Mulai Deteksi" di halaman Home
if st.query_params.get("cta") == "true":
    st.info("👋 Silakan login atau daftar akun terlebih dahulu untuk mulai analisis foto.")
    # Segera hapus param agar pesannya tidak muncul terus-menerus kalau user me-refresh halaman
    st.query_params.clear()

# form login sederhana tanpa styling khusus
email = st.text_input("email")
password = st.text_input("password", type="password")

if st.button("login"):
    if email and password:
        with st.spinner("memverifikasi kredensial..."):
            # memanggil fungsi auth yang sudah kita buat
            success, msg = authenticate_user(email, password)
            
            if success:
                st.success(msg)
                # gunakan time.sleep sebentar agar pesan sukses terlihat sebelum halaman direfresh
                time.sleep(1) 
                # st.rerun wajib dipanggil untuk memicu update pada st.navigation di app.py
                st.rerun() 
            else:
                st.error(msg)
    else:
        st.warning("harap isi email dan password terlebih dahulu.")
import streamlit as st
import time
from session.auth_state import register_user

st.title("registrasi (placeholder)")
st.write("halaman ini digunakan sebagai referensi alur API. nanti bisa diganti UInya.")

# form registrasi sederhana untuk payload fastapi
nama = st.text_input("nama lengkap")
email = st.text_input("email")
password = st.text_input("password", type="password")
konfirmasi_password = st.text_input("konfirmasi password", type="password")

if st.button("daftar akun"):
    # validasi kelengkapan data di sisi klien
    if nama and email and password and konfirmasi_password:
        
        # validasi kecocokan password
        if password == konfirmasi_password:
            with st.spinner("mengirim data ke server..."):
                # mengirim payload ke backend
                success, msg = register_user(nama, email, password)
                
                if success:
                    st.success(msg)
                    time.sleep(1.5)
                    st.switch_page("pages/02_login.py")
                else:
                    st.error(msg)
        else:
            st.warning("password dan konfirmasi password tidak cocok. silakan periksa kembali.")
            
    else:
        st.warning("harap isi semua kolom form yang tersedia.")
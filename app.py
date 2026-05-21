import streamlit as st
import os
from session.auth_state import init_session_state, logout_user, init_auth_state, BILLING_ENABLED

# set konfigurasi global halaman
st.set_page_config(page_title="Acnelytics", page_icon="🔬🔬", layout="centered")

# inisialisasi auth dan session state
init_session_state()
init_auth_state()

# injeksi css global
st.markdown("""
<style>
/* sidebar background putih */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e8edf3;
}
[data-testid="stSidebar"] * {
    color: #1a1a2e !important;
}

/* logo bulat di atas sidebar */
[data-testid="stSidebarNav"]::before {
    content: "";
    display: block;
    background-image: url("https://api.dicebear.com/7.x/shapes/svg?seed=skindetect&backgroundColor=1a6ec8");
    background-size: cover;
    width: 70px; height: 70px;
    border-radius: 50%;
    border: 3px solid #1a6ec8;
    margin: 1.4rem auto 0.5rem auto;
}
[data-testid="stSidebarNav"] ul::before {
    content: "Acnelytics";
    display: block;
    text-align: center;
    font-weight: 700;
    font-size: 1.05rem;
    color: #1a3c6e !important;
    margin-bottom: 1.2rem;
    letter-spacing: 0.02em;
}

/* styling navigasi default */
[data-testid="stSidebarNav"] a {
    border-radius: 10px;
    margin-bottom: 2px;
    color: #1a1a2e !important;
}

/* styling navigasi aktif */
[data-testid="stSidebarNav"] a[aria-selected="true"],
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background-color: rgba(26, 110, 200, 0.12) !important;
    border-radius: 10px;
}
[data-testid="stSidebarNav"] a[aria-selected="true"] span,
[data-testid="stSidebarNav"] a[aria-current="page"] span {
    color: #1a6ec8 !important;
    font-weight: 700;
}

/* hover navigasi */
[data-testid="stSidebarNav"] a:hover {
    background-color: rgba(26, 110, 200, 0.07) !important;
    border-radius: 10px;
}
[data-testid="stSidebarNav"] a:hover span {
    color: #1a6ec8 !important;
}

/* tombol dan font global */
div.stButton > button {
    background-color: #1a6ec8; color: white; border: none; border-radius: 8px;
}
div.stButton > button:hover { background-color: #155ab0; color: white; }
h1, h2, h3, h4 { color: #1a3c6e; }
</style>
""", unsafe_allow_html=True)

# definisi semua halaman aplikasi
login_page = st.Page("pages/02_login.py", title="Login", icon="🔑")
register_page = st.Page("pages/03_register.py", title="Daftar Akun", icon="📝")

home_page = st.Page("pages/01_home.py", title="Home", icon="🔬")
upload_page = st.Page("pages/04_upload.py", title="Upload & Deteksi", icon="📤")
history_page = st.Page("pages/05_history.py", title="Riwayat", icon="🕘")
profile_page = st.Page("pages/06_profile.py", title="Profil Saya", icon="👤")
admin_page = st.Page("pages/08_admin.py", title="Dashboard Admin", icon="⚙️")

# guard dan routing dinamis berdasarkan status login
if not st.session_state.logged_in:
    # user belum login: hanya bisa akses login dan register
    pg = st.navigation(
        [
            home_page,
            login_page, register_page
        ],
        position="sidebar",
        expanded=True
    )
else:
    # user sudah login: sidebar menampilkan menu internal
    
    # render tombol logout di area sidebar bawah
    with st.sidebar:

        # UI billing
        if BILLING_ENABLED:
            billing = st.session_state.get("billing_info", {})
            plan = billing.get("active_plan", "Unknown").replace("_", " ").title()
            quota = billing.get("remaining_quota", 0)
            
            st.markdown("#### 💳 Info Tagihan")
            
            # Beri warna merah jika kuota habis
            quota_color = "red" if quota <= 0 else "#2d8a50"
            
            st.markdown(f"""
            <div style="background:#f8faff; padding:10px; border-radius:8px; border: 1px solid #e8edf3; margin-bottom: 1rem;">
                <div style="font-size: 0.85rem; color: #555;">Paket Saat Ini:</div>
                <div style="font-weight: bold; color: #1a3c6e; margin-bottom: 5px;">{plan}</div>
                <div style="font-size: 0.85rem; color: #555;">Sisa Kuota:</div>
                <div style="font-weight: bold; color: {quota_color}; font-size: 1.1rem;">{quota} Analisis</div>
            </div>
            """, unsafe_allow_html=True)

        # tombol logout
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            logout_user()
            st.rerun()
            
    # cek role untuk menampilkan panel admin (opsional sesuai dokumen arsitektur)
    if st.session_state.role == "admin":
        pg = st.navigation({
            "Menu Utama": [home_page, upload_page, history_page],
            "Pengaturan": [profile_page],
            "Admin Panel": [admin_page]
        })
    else:
        pg = st.navigation({
            "Menu Utama": [home_page, upload_page, history_page],
            "Pengaturan": [profile_page]
        })

# jalankan perutean halaman
pg.run()
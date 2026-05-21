import streamlit as st
import requests
from datetime import datetime
from components.ui_components import apply_global_styles
from services.api_client import get_user_history 

st.set_page_config(page_title="Riwayat Deteksi", page_icon="🕘", layout="centered")
apply_global_styles()

st.markdown("""
<div style="background: linear-gradient(135deg, #1a6ec8, #3a9bd5);
            border-radius: 14px; padding: 1.2rem 1.6rem; margin-bottom: 1.2rem;">
    <h2 style="margin:0; color:white;">🕘 Riwayat Deteksi</h2>
    <p style="margin:0.3rem 0 0; color:#d0eaff; font-size:0.9rem;">Riwayat analisis yang tersimpan di sistem</p>
</div>
""", unsafe_allow_html=True)

# 1. Strict auth guard
token = st.session_state.get("access_token")
if not token:
    st.error("🔒 anda belum login atau sesi telah berakhir.")
    st.stop()

# 2. Tarik data riwayat dari backend
with st.spinner("mengambil data riwayat dari database..."):
    try:
        # Gunakan nama fungsi aslimu
        history_data = get_user_history(token)
    except Exception as e:
        st.error(f"❌ gagal mengambil riwayat: {str(e)}")
        st.stop()

if not history_data or len(history_data) == 0:
    st.warning("belum ada riwayat. silakan upload dan analisis foto di halaman **Upload & Deteksi** terlebih dahulu.")
    st.stop()

st.write(f"{len(history_data)} hasil ditemukan.")
st.markdown("---")

# untuk debugging
# st.json(history_data)

# 3. Render data yang sudah disesuaikan dengan arsitektur Celery + ML Engine
for item in history_data:
    status_job = item.get("status", "error")
    
    col_thumb, col_detail = st.columns([1, 3])

    with col_thumb:
        image_url = item.get("image_url") # Contoh: http://localhost:9000/bucket/img.jpg
        if image_url:
            # Gunakan URL Tailscale FastAPI milikmu
            api_base_url = "https://cationode-ub-01.tail55d5d2.ts.net/api/v1"
            proxy_url = f"{api_base_url}/auth/proxy-image?url={image_url}"
            
            try:
                # Sekarang Streamlit meminta gambar melalui Tailscale FastAPI
                response = requests.get(proxy_url, timeout=10)
                if response.status_code == 200:
                    st.image(response.content, use_container_width=True)
                else:
                    st.warning("⚠️ Gagal memuat gambar dari server.")
            except Exception as e:
                st.error("Terputus dari server API.")
        else:
            st.info("gambar tidak tersedia")

    with col_detail:
        if status_job in ["succeeded"]:
            # Menggunakan key baru dari ml_engine.py
            prediksi = item.get("top_prediction", "unknown").capitalize()
            confidence = item.get("confidence", 0.0)
            tanggal_raw = item.get("created_at", "-")
            
            # Mempercantik format tanggal
            try:
                dt = datetime.fromisoformat(tanggal_raw.replace('Z', '+00:00'))
                tanggal_str = dt.strftime("%d %b %Y, %H:%M WIB")
            except Exception:
                tanggal_str = tanggal_raw

            st.write(f"**{prediksi}** — {confidence * 100:.1f}% confidence")
            st.write(f"🕐 {tanggal_str}  |  📄 {item.get('filename', '-')}")

            with st.expander("Lihat detail & metadata"):
                # Menampilkan JSONB extra_params
                extra_params = item.get("extra_params", {})
                if extra_params:
                    st.write("**Metadata Pengguna:**")
                    st.json(extra_params)
                
                # Menggunakan key baru full_results
                st.write("**Detail Probabilitas:**")
                top_k = item.get("full_results", item.get("top_k", {}))
                if top_k:
                    sorted_scores = sorted(top_k.items(), key=lambda x: float(x[1]), reverse=True)
                    for label, prob in sorted_scores:
                        st.write(f"**{label.capitalize()}** — {prob * 100:.2f}%")
                        st.progress(float(prob))

        elif status_job == "processing":
            st.warning("⏳ Analisis sedang diproses oleh worker di latar belakang.")
            st.write(f"🕐 {item.get('created_at', '-')}  |  📄 {item.get('filename', '-')}")
            
        elif status_job == "queued":
             st.info("🕒 Sedang mengantre untuk diproses.")
             st.write(f"📄 {item.get('filename', '-')}")
             
        else:
            st.error("❌ Analisis gagal diproses.")
            error_msg = item.get("error_message", "Kesalahan tidak diketahui")
            st.write(f"**Pesan Error:** {error_msg}")
            st.write(f"🕐 {item.get('created_at', '-')}  |  📄 {item.get('filename', '-')}")

    st.markdown("---")
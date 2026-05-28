import streamlit as st
from PIL import Image
import time
import json
from services.api_client import upload_image_for_prediction, get_prediction
from session.auth_state import refresh_billing_state, BILLING_ENABLED
from components.ui_components import apply_global_styles

st.set_page_config(page_title="Upload & Deteksi", page_icon="📤", layout="centered")
apply_global_styles()

# 1. UI: HEADER & BANNER
st.markdown("""
<div style="background: linear-gradient(135deg, #1a6ec8, #3a9bd5);
            border-radius: 14px; padding: 1.2rem 1.6rem; margin-bottom: 1.2rem;">
    <h2 style="margin:0; color:white;">📤 Upload & Deteksi</h2>
    <p style="margin:0.3rem 0 0; color:#d0eaff; font-size:0.9rem;">
        Unggah foto kulit untuk dianalisis oleh model klasifikasi
    </p>
</div>
""", unsafe_allow_html=True)

# 2. SECURITY: AUTH GUARD
token = st.session_state.get("access_token")
if not token:
    st.error("🔒 Anda belum login atau sesi telah berakhir.")
    st.stop()

# UI: STATUS KUOTA
if BILLING_ENABLED:
    billing = st.session_state.get("billing_info", {})
    kuota = billing.get("remaining_quota", 0)
    
    token_color = "#2d8a50" if kuota > 3 else ("#e67e22" if kuota > 0 else "#c0392b")
    st.markdown(f"""
    <div style="background:#f0f7ff;border-radius:10px;padding:0.7rem 1.1rem;
                margin-bottom:1rem;display:flex;align-items:center;gap:0.7rem;">
        <span style="font-size:1.3rem;">🪙</span>
        <span style="font-size:0.92rem;color:#333;">
            Kuota tersisa: <b style="color:{token_color};font-size:1.05rem;">{kuota}</b>
            {"&nbsp;— Setiap analisis berhasil memotong 1 kuota." if kuota > 0
             else "&nbsp;— <b style='color:#c0392b;'>Kuota habis!</b> Hubungi admin untuk top-up."}
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Cegah user mengupload jika kuota sudah habis
    if kuota <= 0:
        st.error("❌ Kuota analisis kamu sudah habis. Silakan perbarui paket.")
        st.stop()

# 3. DATA: UPDATE KELAS PENYAKIT
CLASS_DESC = {
    "blackheads": "Bentuknya seperti bintik hitam kecil di pori-pori yang terbuka. Warna hitam itu bukan karena kotoran, tapi karena minyak yang menyumbat pori berubah warna jadi gelap setelah terkena udara luar.",
    "whiteheads": "Muncul sebagai benjolan kecil berwarna putih. Berbeda dengan blackheads, pori-pori ini tertutup rapat oleh kulit, sehingga minyak yang tersumbat tidak kena udara dan tetap putih.",
    "papules": "Jerawat yang mulai meradang. Berupa benjolan merah dan padat yang terasa nyeri atau hangat. Ciri khasnya, jerawat ini belum punya 'mata' atau puncak nanah.",
    "pustules": "Mirip jerawat merah biasa, tapi di bagian tengahnya sudah ada gelembung kecil berisi nanah putih/kekuningan. Tandanya tubuh sedang melawan bakteri di dalam pori-pori.",
    "cyst": "Jenis paling serius. Letaknya jauh di dalam kulit, ukurannya besar, bertekstur lunak, dan sangat sakit. Paling sering meninggalkan bekas/bopeng."
}

# 4. UI: PANDUAN UPLOAD
st.info("""
**📌 Panduan Upload Foto**
- Foto harus berupa **close-up area jerawat** yang jelas dan spesifik pada area bermasalah.
- **Jangan** upload foto acak, foto seluruh wajah dari jauh, atau foto yang tidak relevan.
- Format yang diterima: **JPG, JPEG, PNG**
- Ukuran maksimal: **5 MB**
""")

uploaded_file = st.file_uploader(# 2. SECURITY: AUTH GUARD
    "Pilih foto kulit Anda",
    type=["jpg", "jpeg", "png"],
    help="Hanya JPG, JPEG, PNG — maksimal 5 MB"
)

if uploaded_file is not None:
    if uploaded_file.size > 5 * 1024 * 1024:
        st.error(f"❌ Ukuran file terlalu besar ({uploaded_file.size / 1024 / 1024:.2f} MB). Maksimal 5 MB.")
        st.stop()

    try:
        image = Image.open(uploaded_file).convert("RGB")
    except Exception:
        st.error("❌ File tidak dapat dibaca sebagai gambar.")
        st.stop()

    st.image(image, caption="Preview foto yang diunggah", use_container_width=True)
    st.markdown("---")

    if st.button("🔍 Analisis Foto Ini", use_container_width=True):
        image_bytes = uploaded_file.getvalue()
        
        # 5. LOGIKA: PREPARE EXTRA DATA
        user_metadata = st.session_state.get("profil", {})
        extra_data_json = json.dumps(user_metadata)
        
        # 6. LOGIKA: API CALL & POLLING
        try:
            # Blok spinner hanya untuk memanggil API
            with st.spinner("Mengirim citra ke server..."):
                # Pastikan fungsi upload_image_for_prediction di api_client.py 
                # sudah dimodifikasi untuk menerima argument `extra_data`
                api_res = upload_image_for_prediction(
                    image_bytes, 
                    uploaded_file.name, 
                    token, 
                    extra_data=extra_data_json
                )
                # Spinner otomatis hilang di sini

            job_id = api_res.get("job_id")
            if not job_id:
                st.error("❌ Gagal mendapatkan job_id dari server.")
                st.stop()
        
        except ValueError as ve:
            st.warning(f"⚠️ {str(ve)}")
            st.stop()

        except Exception as e:
            st.error(f"❌ Gagal menghubungi server: {str(e)}")
            st.stop()
            
        status_placeholder = st.empty()
        max_retries = 30
        attempt = 0
        delay = 1.0       
        max_delay = 8.0   
        final_result = None
        max_error_retries = 2
        error_count = 0

        while attempt < max_retries:
            status_placeholder.info(f"⏳ Memproses model (job id: {job_id}). harap tunggu... (percobaan {attempt+1}/{max_retries})")
            
            try:
                response = get_prediction(job_id, token)
                status = response.get("status")
                
                if status == "succeeded":
                    # Menyesuaikan dengan response FastAPI backend 
                    final_result = response.get("result", response) 
                    status_placeholder.empty()
                    break
                elif status == "failed":
                    error_msg = response.get("error") or "gagal memproses gambar pada worker."
                    status_placeholder.error(f"❌ terjadi kesalahan: {error_msg}")
                    st.stop()
            except Exception as e:
                error_count += 1
                if error_count <= max_error_retries:
                    status_placeholder.warning(f"⚠️ error komunikasi ({error_count}/{max_error_retries}), retry...")
                    time.sleep(1)  
                    continue
                else:
                    status_placeholder.error(f"❌ gagal setelah beberapa percobaan: {str(e)}")
                    st.stop()
                
            time.sleep(delay)
            attempt += 1
            delay = min(delay * 1.5, max_delay)
            
        if not final_result:
            status_placeholder.error("❌ timeout. server memakan waktu terlalu lama.")
            st.stop()

        # 7. UI: RENDER HASIL
        st.success("✅ Analisis selesai dan otomatis tersimpan di database!")
        
        # Panggil API untuk refresh saldo kuota terbaru dari database
        if BILLING_ENABLED:
            refresh_billing_state()
            kuota_baru = st.session_state.get("billing_info", {}).get("remaining_quota", 0)
            
            st.markdown(f"""
            <div style="background:#fffbe6;border-radius:8px;padding:0.5rem 1rem;
                        font-size:0.88rem;color:#7a5c00;margin-bottom:0.5rem;">
                🪙 1 kuota digunakan. Sisa kuota: <b>{kuota_baru}</b>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("---")

        st.subheader("Hasil Deteksi")
        
        # Ambil nilai langsung dari JSON hasil output ml_engine.py yang baru
        top_label = final_result.get("top_prediction", "Unknown")
        top_conf = final_result.get("confidence", 0.0)
        
        st.write(f"**Prediksi:** {top_label.capitalize()}")
        st.write(f"**Confidence:** {top_conf * 100:.1f}%")
        
        deskripsi = CLASS_DESC.get(top_label.lower(), "Deskripsi detail belum tersedia untuk klasifikasi ini.")
        st.write(f"_{deskripsi}_")

        st.markdown("---")
        st.subheader("Detail Top-K")
        
        # Ambil data probabilitas semua kelas
        scores_dict = final_result.get("full_results", final_result.get("top_k", {}))
        sorted_scores = sorted(scores_dict.items(), key=lambda x: float(x[1]), reverse=True)
        
        for label, prob in sorted_scores:
            # sembunyikan 'normal' dari daftar progress bar JIKA dia bukan prediksi utama
            if label.lower() == "normal" and top_label.lower() != "normal":
                continue

            st.write(f"**{label.capitalize()}** — {prob * 100:.2f}%")
            st.progress(float(prob))

        st.markdown("---")
        
        # 8. UI: MEDICAL DISCLAIMER
        st.info("""
        ⚕️ **Perhatian Medis**
        Hasil ini merupakan estimasi berbasis *analisis citra digital* dan **bukan merupakan diagnosis medis**.
        Untuk penanganan yang tepat, konsultasikan kondisi kulit Anda kepada **dokter spesialis kulit (dermatologis)**.
        """)
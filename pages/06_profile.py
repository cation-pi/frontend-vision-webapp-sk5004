import streamlit as st
from collections import Counter
from datetime import datetime
from components.ui_components import apply_global_styles

# Helper function untuk age
def parse_age(value):
    try:
        age = int(value)
        return age if age > 0 else None
    except (TypeError, ValueError):
        return None

# Import dari api_client.py
from services.api_client import get_current_user, update_user_profile, get_user_history

st.set_page_config(page_title="Profil", page_icon="👤", layout="centered")
apply_global_styles() 

# ── HEADER
st.markdown("""
<div style="background: linear-gradient(135deg, #1a6ec8, #3a9bd5);
            border-radius: 14px; padding: 1.2rem 1.6rem; margin-bottom: 1.2rem;">
    <h2 style="margin:0; color:white;">👤 Profil Saya</h2>
    <p style="margin:0.3rem 0 0; color:#d0eaff; font-size:0.9rem;">Catatan pribadi & ringkasan aktivitasmu</p>
</div>
""", unsafe_allow_html=True)

# ── 1. SECURITY: Auth Guard
token = st.session_state.get("access_token")
if not token:
    st.error("🔒 Anda belum login atau sesi telah berakhir.")
    st.stop()

# ── 2. FETCHING DATA: Ambil Profil & Riwayat Aktual dari Database
with st.spinner("Menyiapkan ruang kerjamu..."):
    # Ambil Profil
    if "profil_fetched" not in st.session_state:
        try:
            current_user_data = get_current_user(token)
            st.session_state.profil = {
                "nama": current_user_data.get("nama", ""), 
                "usia": str(current_user_data.get("age", "")) if current_user_data.get("age") is not None else "",
                "jenis_kulit": current_user_data.get("skin_type", ""),
                "catatan": current_user_data.get("notes", "")
            }
            st.session_state.profil_fetched = True
        except Exception as e:
            st.error(f"❌ Gagal mengambil profil: {str(e)}")
            st.stop()
    
    # Ambil Riwayat untuk Statistik
    try:
        history_data = get_user_history(token)
    except:
        history_data = []

profil = st.session_state.profil
jumlah_scan = len(history_data)
nama_tampil = profil["nama"] if profil["nama"] else "Pengguna"

# ── 3. UI: KARTU SAMBUTAN PERSONAL
st.markdown(f"""
<div style="background:#f0f7ff; border-radius:14px; padding:1.2rem 1.4rem; margin-bottom:1rem;
            display:flex; align-items:center; gap:1rem;">
    <div style="font-size:2.8rem; line-height:1;">👋</div>
    <div>
        <div style="font-weight:700; font-size:1.1rem; color:#1a3c6e;">Halo, {nama_tampil}!</div>
        <div style="font-size:0.88rem; color:#555; margin-top:2px;">
            {"Kamu sudah melakukan " + str(jumlah_scan) + " analisis sejauh ini." if jumlah_scan > 0
             else "Belum ada analisis yang tersimpan. Yuk mulai dari halaman Upload & Deteksi!"}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── 4. UI: RINGKASAN AKTIVITAS (Berdasarkan Data Asli)
if jumlah_scan > 0:
    # Filter hanya job yang sukses untuk dihitung statistiknya
    succeeded_scans = [item for item in history_data if item.get("status") == "succeeded"]
    
    if succeeded_scans:
        labels = [item.get("top_prediction", "Unknown").capitalize() for item in succeeded_scans]
        label_counts = Counter(labels)
        top_label = label_counts.most_common(1)[0][0]
        
        # Ambil waktu dari item pertama (asumsi backend mengirim data terbaru di urutan pertama)
        tanggal_raw = succeeded_scans[0].get("created_at", "-")
        try:
            dt = datetime.fromisoformat(tanggal_raw.replace('Z', '+00:00'))
            last_scan_str = dt.strftime("%d %b %Y")
        except:
            last_scan_str = tanggal_raw.split("T")[0]
    else:
        top_label = "-"
        label_counts = Counter()
        last_scan_str = "-"

    st.markdown("#### 📊 Ringkasan Aktivitas")
    ca, cb, cc = st.columns(3)
    with ca:
        st.markdown(f"""
        <div style="background:#eaf3fb; border-radius:12px; padding:1rem; text-align:center;">
            <div style="font-size:1.6rem;">🔍</div>
            <div style="font-weight:700; color:#1a3c6e; font-size:1.3rem;">{jumlah_scan}</div>
            <div style="font-size:0.78rem; color:#666;">Total upload</div>
        </div>
        """, unsafe_allow_html=True)
    with cb:
        st.markdown(f"""
        <div style="background:#eaf3fb; border-radius:12px; padding:1rem; text-align:center;">
            <div style="font-size:1.6rem;">🏷️</div>
            <div style="font-weight:700; color:#1a3c6e; font-size:1rem;">{top_label}</div>
            <div style="font-size:0.78rem; color:#666;">Hasil terbanyak</div>
        </div>
        """, unsafe_allow_html=True)
    with cc:
        st.markdown(f"""
        <div style="background:#eaf3fb; border-radius:12px; padding:1rem; text-align:center;">
            <div style="font-size:1.6rem;">🕐</div>
            <div style="font-weight:700; color:#1a3c6e; font-size:0.78rem;">{last_scan_str}</div>
            <div style="font-size:0.78rem; color:#666;">Analisis terakhir</div>
        </div>
        """, unsafe_allow_html=True)

    # Distribusi hasil
    if label_counts:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Distribusi hasil deteksi (yang berhasil diproses):**")
        total_succeeded = len(succeeded_scans)
        for label, count in label_counts.most_common():
            pct = count / total_succeeded
            st.write(f"**{label}** — {count}x ({pct*100:.0f}%)")
            st.progress(pct)

    st.markdown("---")

# ── 5. FORM PROFIL (Terhubung ke API)
st.markdown("#### ✏️ Informasi Pribadi")
st.markdown("<p style='font-size:0.88rem; color:#666; margin-bottom:0.8rem;'>"
            "Informasi ini akan disimpan secara permanen dan otomatis disertakan sebagai metadata saat sistem AI melakukan analisis citra.</p>",
            unsafe_allow_html=True)

nama          = st.text_input("Nama", value=profil["nama"], placeholder="contoh: Andi")
usia          = st.text_input("Usia", value=profil["usia"], placeholder="contoh: 22")
pilihan_kulit = ["", "Normal", "Berminyak", "Kering", "Kombinasi", "Sensitif"]
idx           = pilihan_kulit.index(profil["jenis_kulit"]) if profil["jenis_kulit"] in pilihan_kulit else 0
jenis_kulit   = st.selectbox("Jenis Kulit (opsional)", options=pilihan_kulit, index=idx)
catatan       = st.text_area("Catatan Tambahan (opsional)", value=profil["catatan"], 
                             placeholder="Misal: kulit mudah kemerahan, sedang memakai krim malam dokter...", height=100)

if st.button("💾 Simpan Profil", use_container_width=True):
    with st.spinner("Menyimpan ke pangkalan data..."):
        payload = {
            "nama": nama,
            "age": parse_age(usia),
            "skin_type": jenis_kulit if jenis_kulit else None,
            "notes": catatan if catatan else None
        }
        
        try:
            update_user_profile(token, payload)
            
            st.session_state.profil = {
                "nama": nama, 
                "usia": usia, 
                "jenis_kulit": jenis_kulit, 
                "catatan": catatan
            }
            st.success("✅ Profil berhasil disimpan permanen!")
        except Exception as e:
            st.error(f"❌ Gagal menyimpan profil: {str(e)}")

st.markdown("---")

# ── 6. RENDER DATA TERSIMPAN (Dari UI FE)
if profil["nama"] or profil["catatan"]:
    st.markdown("#### 📋 Catatan Medis/Pribadi")
    if profil["nama"]:
        st.write(f"**Nama:** {profil['nama']}")
    if profil["usia"]:
        st.write(f"**Usia:** {profil['usia']} tahun")
    if profil["jenis_kulit"]:
        st.write(f"**Jenis Kulit:** {profil['jenis_kulit']}")
    if profil["catatan"]:
        st.markdown(f"""
        <div style="background:#f8faff; border-radius:10px; padding:0.9rem 1.1rem;
                    border-left:3px solid #1a6ec8; font-size:0.91rem; color:#333; line-height:1.6;">
            {profil["catatan"]}
        </div>
        """, unsafe_allow_html=True)
import streamlit as st
from components.ui_components import apply_global_styles

st.set_page_config(page_title="Acnelytics", page_icon="🔬", layout="centered")
apply_global_styles() 

# ── 1. HERO — Orientasi pertama: ini apa & mau ngapain

# Tentukan target URL secara dinamis
is_logged_in = st.session_state.get("logged_in", False)

if is_logged_in:
    target_url = "/upload" 
else:
    # Kirim sinyal cta=true agar halaman login tau user datang dari tombol ini
    target_url = "/login?cta=true"

st.markdown(f"""
<div style="background: linear-gradient(135deg, #1a6ec8, #3a9bd5);
            border-radius: 16px; padding: 2.2rem 2rem 1.8rem; margin-bottom: 1.2rem; text-align:center;">
    <div style="font-size:2.8rem; margin-bottom:0.4rem;">🔬</div>
    <h1 style="margin:0; font-size:2rem; color:white; letter-spacing:-0.5px;">Acnelytics</h1>
    <p style="margin:0.5rem auto 0.3rem; color:#d0eaff; font-size:1rem; max-width:420px;">
        Upload foto jerawatmu, dan AI kami akan membantu mengidentifikasi jenisnya
        dalam hitungan detik.
    </p>
    <br>
    <a href="{target_url}" target="_self"
       style="display:inline-block; background:white; color:#1a6ec8; font-weight:700;
              padding:0.55rem 1.6rem; border-radius:999px; text-decoration:none; font-size:0.95rem;">
        📤 Mulai Deteksi
    </a>
</div>
""", unsafe_allow_html=True)

# ── 2. TRUST SIGNAL — angka singkat biar user tahu scope-nya
c1, c2, c3 = st.columns(3)
for col, icon, val, label in zip(
    [c1, c2, c3],
    ["🧬", "⚡", "🎯"],
    ["5 Jenis", "Cepat", "Top-K Detail"],
    ["Jerawat terdeteksi", "Hasil dalam beberapa detik", "Hasil per kelas"]
):
    with col:
        st.markdown(f"""
        <div style="background:#eaf3fb; border-radius:12px; padding:1rem; text-align:center;">
            <div style="font-size:1.6rem;">{icon}</div>
            <div style="font-weight:700; color:#1a3c6e; font-size:1rem; margin:0.2rem 0;">{val}</div>
            <div style="font-size:0.78rem; color:#666;">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# ── 3. KELAS JERAWAT — user mulai paham konteks sebelum upload
st.markdown("#### 🧬 Jenis Jerawat yang Dapat Dideteksi")
st.markdown("<p style='color:#666; font-size:0.88rem; margin-bottom:0.8rem;'>"
            "Klik untuk lihat penjelasan, ciri khas, dan saran umum.</p>",
            unsafe_allow_html=True)

KELAS = [
    ("⚫", "Blackhead", "#2c2c2c", "#f3f3f3",
     "Bintik hitam kecil yang muncul di permukaan pori-pori terbuka.",
     ["Warnanya hitam karena minyak yang menyumbat pori berubah gelap setelah teroksidasi oleh udara, bukan karena kotoran.",
      "Umumnya tidak terasa nyeri dan tidak meradang.",
      "Paling sering muncul di area hidung, dagu, dan dahi."],
     "Hindari menyentuh atau memencet area yang terdampak karena bisa mendorong kotoran lebih dalam dan memperparah kondisi."),
    ("⚪", "Whitehead", "#555", "#f8f8f8",
     "Benjolan kecil berwarna putih atau sewarna kulit.",
     ["Pori-pori tertutup rapat oleh lapisan kulit sehingga minyak di dalamnya tidak teroksidasi.",
      "Terlihat seperti titik putih kecil yang sedikit menonjol.",
      "Biasanya tidak meradang dan tidak terasa sakit."],
     "Jangan dipaksa pecah karena tekanan dari luar bisa menyebabkan peradangan dan meninggalkan bekas."),
    ("🔴", "Papule", "#c0392b", "#fff0f0",
     "Benjolan merah padat yang terasa nyeri, tanpa nanah di dalamnya.",
     ["Tanda awal jerawat meradang — area sekitarnya bisa terasa hangat dan sensitif saat disentuh.",
      "Terbentuk ketika dinding pori-pori pecah akibat tekanan dari dalam.",
      "Belum ada nanah yang terlihat di permukaan."],
     "Hindari memencet karena bisa memperparah peradangan dan memperluas penyebaran bakteri ke area sekitarnya."),
    ("🟡", "Pustule", "#b8860b", "#fffbe6",
     "Benjolan merah dengan gelembung nanah putih atau kekuningan di tengahnya.",
     ["Nanah yang terbentuk adalah respons alami tubuh dalam melawan bakteri di dalam pori.",
      "Terasa nyeri jika disentuh dan area sekitarnya tampak kemerahan.",
      "Lebih besar dan lebih menonjol dibanding papule."],
     "Biarkan proses alami tubuh bekerja. Memencet dengan cara yang salah bisa mendorong infeksi lebih dalam dan meninggalkan bekas."),
    ("🔵", "Cyst", "#1a6ec8", "#eaf3fb",
     "Benjolan besar, terasa lunak seperti balon berisi cairan, dan sangat nyeri.",
     ["Jenis jerawat paling serius — infeksi terjadi jauh di bawah permukaan kulit.",
      "Ukurannya lebih besar dari jenis lain dan terasa empuk saat ditekan.",
      "Paling berisiko meninggalkan bekas atau bopeng permanen setelah sembuh."],
     "Karena letaknya dalam dan berisiko tinggi meninggalkan bekas, sangat tidak disarankan menangani sendiri tanpa panduan dari tenaga medis."),
]

for icon, nama, warna, bg, singkat, ciri_list, saran in KELAS:
    with st.expander(f"{icon} **{nama}**"):
        st.markdown(f"""
        <div style="border-left:4px solid {warna}; background:{bg};
                    border-radius:0 10px 10px 0; padding:0.9rem 1.1rem; margin-bottom:0.6rem;">
            <b style="color:{warna}; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.06em;">Apa itu?</b>
            <p style="margin:0.3rem 0 0; font-size:0.91rem; color:#333;">{singkat}</p>
        </div>
        <div style="background:#f8f8f8; border-radius:10px; padding:0.9rem 1.1rem; margin-bottom:0.6rem;">
            <b style="font-size:0.8rem; text-transform:uppercase; letter-spacing:0.06em; color:#444;">📌 Ciri</b>
            <ul style="margin:0.4rem 0 0; padding-left:1.2rem; font-size:0.9rem; color:#333; line-height:1.8;">
                {" ".join(f"<li>{c}</li>" for c in ciri_list)}
            </ul>
        </div>
        <div style="background:#f0f7ff; border-radius:10px; padding:0.9rem 1.1rem;">
            <b style="color:#1a6ec8; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.06em;">💡 Saran Umum</b>
            <p style="margin:0.3rem 0 0; font-size:0.91rem; color:#333;">{saran}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ── 4. TIPS FOTO — persiapan sebelum upload
st.markdown("#### 📸 Tips Foto agar Hasil Lebih Akurat")
col_a, col_b = st.columns(2)
with col_a:
    st.markdown("""
    <div style="background:#edfaf1; border-radius:12px; padding:1rem 1.1rem; height:100%;">
        <b style="color:#2d8a50;">✅ Lakukan ini</b>
        <ul style="margin:0.5rem 0 0; padding-left:1.2rem; font-size:0.88rem; color:#333; line-height:1.8;">
            <li>Foto di tempat terang, pencahayaan alami</li>
            <li>Jarak kamera 10–15 cm dari kulit</li>
            <li>Fokus pada area jerawat yang spesifik</li>
            <li>Gambar tajam dan tidak blur</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
with col_b:
    st.markdown("""
    <div style="background:#fff0f0; border-radius:12px; padding:1rem 1.1rem; height:100%;">
        <b style="color:#c0392b;">❌ Hindari ini</b>
        <ul style="margin:0.5rem 0 0; padding-left:1.2rem; font-size:0.88rem; color:#333; line-height:1.8;">
            <li>Foto seluruh wajah dari jauh</li>
            <li>Foto gelap, blur, atau terlalu terang</li>
            <li>Ada filter atau efek kamera</li>
            <li>Foto yang bukan area kulit bermasalah</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── 5. LANGKAH PAKAI — sekarang user siap, tunjukkan caranya
st.markdown("#### 📋 Cara Menggunakan Acnelytics")
steps = [
    ("1", "🖼️", "Upload Foto", "Pilih foto close-up (JPG/PNG, maks. 5 MB)"),
    ("2", "🔍", "Klik Analisis", "Tekan tombol & tunggu beberapa detik"),
    ("3", "📊", "Baca Hasilnya", "Prediksi + confidence + Top-K perbandingan"),
    ("4", "🕘", "Cek Riwayat", "Semua hasil tersimpan otomatis"),
]
cols = st.columns(4)
for col, (num, icon, judul, sub) in zip(cols, steps):
    with col:
        st.markdown(f"""
        <div style="text-align:center; padding:0.8rem 0.3rem;">
            <div style="width:36px; height:36px; border-radius:50%; background:#1a6ec8;
                        color:white; font-weight:700; font-size:1rem; line-height:36px;
                        margin:0 auto 0.4rem;">{num}</div>
            <div style="font-size:1.3rem;">{icon}</div>
            <div style="font-weight:600; font-size:0.83rem; color:#1a3c6e; margin-top:0.3rem;">{judul}</div>
            <div style="font-size:0.74rem; color:#777; margin-top:3px; line-height:1.4;">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ── 6. FAQ — setelah paham caranya, user mulai punya pertanyaan
st.markdown("#### ❓ Pertanyaan yang Sering Ditanyakan")
faqs = [
    ("Apakah hasil deteksi ini akurat?",
     "Model kami dilatih pada dataset citra jerawat dan mampu memberikan estimasi yang cukup baik. Namun akurasi sangat bergantung pada kualitas foto yang diunggah. Semakin jelas dan fokus fotonya, semakin relevan hasilnya. Gunakan hasil ini sebagai referensi awal, bukan diagnosis pasti."),
    ("Apakah foto saya disimpan?",
     "Tidak. Foto yang kamu upload hanya diproses di sesi yang sedang berjalan dan tidak disimpan ke server manapun. Setelah sesi berakhir atau browser ditutup, semua data hilang otomatis."),
    ("Mengapa hasilnya bisa berbeda untuk foto yang sama?",
     "Model menganalisis pola visual secara statistik. Sedikit perbedaan sudut, cahaya, atau resolusi foto bisa menghasilkan prediksi yang berbeda. Ini adalah keterbatasan wajar dari sistem berbasis AI."),
    ("Apa itu Confidence Score?",
     "Confidence Score adalah angka (biasanya dari 0-100%) yang menunjukkan seberapa yakin model AI dengan prediksinya. Score tinggi (misal >80%) berarti model sangat yakin, sementara score rendah menunjukkan ketidakpastian."),
    ("Apa itu Top-K?",
     "Top-K adalah daftar beberapa prediksi teratas yang paling mungkin, beserta confidence score masing-masing. Ini berguna untuk melihat apakah ada beberapa jenis jerawat yang memiliki kemiripan tinggi di mata model AI."),
    ("Apakah Acnelytics bisa menggantikan dokter?",
     "Tidak, dan memang tidak dirancang untuk itu. Acnelytics adalah alat bantu informasi awal. Untuk diagnosis dan penanganan yang tepat, tetap konsultasikan ke dokter spesialis kulit."),
]
for pertanyaan, jawaban in faqs:
    with st.expander(f"❓ {pertanyaan}"):
        st.markdown(f"""
        <div style="background:#f8faff; border-radius:10px; padding:0.9rem 1.1rem;
                    font-size:0.91rem; color:#333; line-height:1.7; border-left:3px solid #1a6ec8;">
            {jawaban}
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ── 7. DISCLAIMER — paling bawah, setelah user sudah paham semuanya
st.markdown("""
<div style="background:#f0f7ff; border-radius:12px; padding:1.1rem 1.3rem;
            border-left: 4px solid #1a6ec8;">
    <b style="color:#1a3c6e;">⚕️ Penting untuk Diketahui</b>
    <p style="margin:0.5rem 0 0.8rem; font-size:0.88rem; color:#444; line-height:1.6;">
        Acnelytics menggunakan model <b>deep learning berbasis Computer Vision</b> untuk menganalisis citra kulit dan mengidentifikasi jenis jerawat.
        Output berupa prediksi kelas utama beserta confidence score dan perbandingan Top-K kelas.
    </p>
    <p style="margin:0 0 0.8rem; font-size:0.88rem; color:#444; line-height:1.6;">
        Namun, ini adalah <b>alat bantu informasi berbasis AI</b>, bukan diagnosis medis resmi.
        Hasil yang diberikan <b>tidak menggantikan pemeriksaan langsung</b> oleh tenaga medis.
        Akurasi juga sangat bergantung pada kualitas foto (tidak buram, pencahayaan baik, fokus pada area spesifik).
    </p>
    <p style="margin:0; font-size:0.88rem; color:#444; line-height:1.6;">
        Jika jerawatmu terasa nyeri, menyebar luas, atau sudah berlangsung lama —
        segera konsultasikan ke <b>dokter spesialis kulit (dermatologis)</b>.
    </p>
</div>
""", unsafe_allow_html=True)
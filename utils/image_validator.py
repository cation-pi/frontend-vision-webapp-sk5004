import streamlit as st

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_FILE_SIZE_MB = 5

def validate_uploaded_image(uploaded_file):
    """
    Memvalidasi ekstensi dan ukuran file yang diunggah.
    Mengembalikan (True, "") jika valid, atau (False, "pesan error") jika tidak valid.
    """
    if uploaded_file is None:
        return False, "Tidak ada file yang diunggah."

    # Cek ekstensi
    file_extension = uploaded_file.name.split(".")[-1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        return False, f"Format file tidak didukung. Gunakan: {', '.join(ALLOWED_EXTENSIONS)}"

    # Cek ukuran file
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        return False, f"Ukuran file terlalu besar ({file_size_mb:.1f} MB). Maksimal {MAX_FILE_SIZE_MB} MB."

    return True, "File valid."
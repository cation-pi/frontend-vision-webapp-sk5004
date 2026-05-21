import streamlit as st

def apply_global_styles():
    """Fungsi ini memuat semua CSS kustom dari desain UI/UX."""
    st.markdown("""
    <style>
    /* Sidebar background putih */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e8edf3;
    }
    [data-testid="stSidebar"] * {
        color: #1a1a2e !important;
    }

    /* Logo bulat di atas sidebar */
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

    /* Semua item nav — teks hitam default */
    [data-testid="stSidebarNav"] a {
        border-radius: 10px;
        margin-bottom: 2px;
        color: #1a1a2e !important;
    }
    [data-testid="stSidebarNav"] a span {
        color: #1a1a2e !important;
        font-weight: 400;
    }

    /* Item aktif — teks biru + bg biru transparan */
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

    /* Hover item */
    [data-testid="stSidebarNav"] a:hover {
        background-color: rgba(26, 110, 200, 0.07) !important;
        border-radius: 10px;
    }
    [data-testid="stSidebarNav"] a:hover span {
        color: #1a6ec8 !important;
    }

    div.stButton > button {
        background-color: #1a6ec8; color: white; border: none; border-radius: 8px;
    }
    div.stButton > button:hover { background-color: #155ab0; color: white; }
    h1, h2, h3, h4 { color: #1a3c6e; }
    </style>
    """, unsafe_allow_html=True)
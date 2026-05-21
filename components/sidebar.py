import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.title("🩺 SkinDetect AI")
        st.markdown("---")
        
        if "user_data" in st.session_state and st.session_state["user_data"]:
            user_name = st.session_state["user_data"].get("nama", "User")
            st.success(f"Masuk sebagai: **{user_name}**")
            
            if st.button("Logout", use_container_width=True):
                # Bersihkan semua sesi saat logout
                st.session_state.clear()
                st.rerun()
        else:
            st.info("Silakan login untuk menggunakan fitur deteksi.")
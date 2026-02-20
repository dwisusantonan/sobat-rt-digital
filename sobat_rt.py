import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Sobat RT Digital", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS FOR MODERN UI ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #4F46E5; color: white; }
    .stat-card { padding: 20px; border-radius: 15px; background-color: white; border: 1px solid #e5e7eb; }
    </style>
    """, unsafe_allow_html=True)

# --- MOCK DATABASE (Session State) ---
if 'data_warga' not in st.session_state:
    st.session_state.data_warga = [
        {"Rumah": "A-01", "Nama": "Budi Santoso", "Keluarga": 4, "Kendaraan": "Mobil (B 1234 RT)", "Iuran": "Lunas"},
        {"Rumah": "A-02", "Nama": "Siti Aminah", "Keluarga": 3, "Kendaraan": "Motor (B 9999 AB)", "Iuran": "Pending"},
        {"Rumah": "B-05", "Nama": "Andi Wijaya", "Keluarga": 5, "Kendaraan": "Mobil (B 8888 ZZ)", "Iuran": "Belum Bayar"}
    ]

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🏙️ Sobat RT")
    st.subheader("Digitalisasi Tetangga")
    role = st.selectbox("Masuk Sebagai:", ["Warga (User)", "Pengurus (Admin)"])
    st.divider()
    st.info("Sobat RT membantu transparansi iuran dan pendataan warga secara real-time.")

# --- APP LOGIC ---

# --- INTERFACE: WARGA ---
if role == "Warga (User)":
    st.header("👋 Selamat Datang, Warga!")
    
    tab1, tab2, tab3 = st.tabs(["📊 Status Saya", "📝 Update Biodata", "📢 Pengumuman"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.metric("Status Iuran Februari", "Lunas ✅")
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.metric("Total Anggota Keluarga", "4 Orang")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.subheader("💳 Bayar Iuran")
        uploaded_file = st.file_uploader("Upload Bukti Transfer (JPG/PNG)", type=['png', 'jpg'])
        if uploaded_file and st.button("Kirim Bukti Pembayaran"):
            st.success("Bukti terkirim! Admin akan memverifikasi dalam 1x24 jam.")

    with tab2:
        st.subheader("🔄 Update Data Keluarga & Kendaraan")
        with st.form("form_biodata"):
            nama = st.text_input("Nama Kepala Keluarga", "Budi Santoso")
            jml_keluarga = st.number_input("Jumlah Anggota Keluarga", min_value=1, value=4)
            kendaraan = st.text_area("Detail Kendaraan (Merk/Plat)", "Mobil Toyota (B 1234 RT)")
            if st.form_submit_button("Simpan Perubahan"):
                st.balloons()
                st.success("Data berhasil diperbarui di sistem RT.")

    with tab3:
        st.info("**📢 Info Kerja Bakti:** Minggu depan, jam 07:00. Mohon partisipasinya.")

# --- INTERFACE: ADMIN ---
else:
    st.header("🛠️ Dashboard Pengurus RT")
    
    # Financial Stats
    c1, c2, c3 = st.columns(3)
    c1.metric("Kas Terkumpul", "Rp 4.500.000", "+Rp 500rb")
    c2.metric("Tunggakan", "Rp 1.200.000", "-10%")
    c3.metric("Laporan Masuk", "2 Bukti Bayar", delta_color="normal")

    st.subheader("📋 Manajemen Warga & Iuran")
    df = pd.DataFrame(st.session_state.data_warga)
    st.dataframe(df, use_container_width=True)

    st.subheader("✅ Verifikasi Pembayaran")
    pending_list = [w for w in st.session_state.data_warga if w['Iuran'] == 'Pending']
    if pending_list:
        for p in pending_list:
            col_a, col_b = st.columns([3, 1])
            col_a.write(f"Bukti Bayar dari: **{p['Nama']}** (Rumah {p['Rumah']})")
            if col_b.button(f"Setujui {p['Rumah']}", key=p['Rumah']):
                st.toast(f"Iuran {p['Rumah']} berhasil diverifikasi!")
    else:
        st.write("Semua bukti pembayaran sudah diproses.")

    st.subheader("📈 Laporan Keuangan (Export)")
    st.button("Download Laporan PDF")
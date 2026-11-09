import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman (Wide Layout)
st.set_page_config(page_title="Dashboard Akademik Profesional", layout="wide")

st.title("🎓 Dashboard Analisis Kinerja Akademik Mahasiswa")
st.markdown("Portofolio Interaktif *Data Analyst* — Memvisualisasikan Faktor Penentu IPK Mahasiswa.")

# Fitur Upload Dataset
uploaded_file = st.file_uploader("📂 Upload file dataset Anda (Data Mahasiswa.csv)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # --- 1. KARTU RINGKASAN METRIK (KPI CARDS) ---
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Mahasiswa", f"{len(df):,} Jiwa")
    with col2:
        st.metric("Rata-rata IPK", f"{df['IPK'].mean():.2f}")
    with col3:
        st.metric("Rata-rata Kehadiran", f"{df['Kehadiran (%)'].mean():.1f}%")
    with col4:
        lulus_count = (df['Status Akademik'] == 'Lulus').sum()
        persen_lulus = (lulus_count / len(df)) * 100
        st.metric("Tingkat Kelulusan", f"{persen_lulus:.1f}%")
    st.markdown("---")

    # --- 2. PREVIEW DATA INTERAKTIF ---
    st.subheader("📋 Preview Data Mahasiswa")
    pilihan_tampilan = st.radio(
        "Pilih metode tampilan data:", 
        ["25 Data Teratas", "25 Data Acak (Random)"],
        horizontal=True
    )
    
    if pilihan_tampilan == "25 Data Teratas":
        st.dataframe(df.head(25), use_container_width=True)
    else:
        jumlah_sampel = min(25, len(df))
        st.dataframe(df.sample(n=jumlah_sampel, random_state=42), use_container_width=True)
        
    st.markdown("---")
    
    # --- 3. GRAFIK INTERAKTIF PLOTLY (PROFESSIONAL LOOK) ---
    st.subheader("📊 Visualisasi & Analisis Interaktif")
    
    row1_col1, row1_col2 = st.columns(2)
    
    with row1_col1:
        # Grafik 1: Histogram Distribusi IPK berdasarkan Status Akademik
        fig_hist = px.histogram(
            df, x="IPK", color="Status Akademik",
            marginal="box", # Menambahkan boxplot di atas histogram
            title="<b>Distribusi IPK Berdasarkan Status Akademik</b>",
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={"IPK": "Indeks Prestasi Kumulatif (IPK)"}
        )
        fig_hist.update_layout(bargap=0.1, template="plotly_white")
        st.plotly_chart(fig_hist, use_container_width=True)
        
    with row1_col2:
        # Grafik 2: Scatter Plot Interaktif Kehadiran vs IPK dengan Ukuran Nilai Tugas
        fig_scatter = px.scatter(
            df, x="Kehadiran (%)", y="IPK",
            color="Status Akademik",
            size="Nilai Tugas (rata-rata)",
            hover_data=["Nama", "Aktivitas E-Learning (skor)"],
            title="<b>Korelasi Kehadiran vs IPK (Ukuran = Nilai Tugas)</b>",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_scatter.update_layout(template="plotly_white")
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    row2_col1, row2_col2 = st.columns(2)
    
    with row2_col1:
        # Grafik 3: Box Plot Perbandingan IPK Berdasarkan Jenis Kelamin
        fig_box = px.box(
            df, x="Jenis Kelamin", y="IPK", color="Status Menikah",
            title="<b>Sebaran IPK Berdasarkan Jenis Kelamin & Status Menikah</b>",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_box.update_layout(template="plotly_white")
        st.plotly_chart(fig_box, use_container_width=True)
        
    with row2_col2:
        # Grafik 4: Scatter Plot Aktivitas E-Learning vs Partisipasi Diskusi
        fig_bubble = px.scatter(
            df, x="Partisipasi Diskusi (skor)", y="Aktivitas E-Learning (skor)",
            color="IPK",
            title="<b>Hubungan Partisipasi Diskusi & Aktivitas E-Learning (Skala Warna = IPK)</b>",
            color_continuous_scale="Viridis"
        )
        fig_bubble.update_layout(template="plotly_white")
        st.plotly_chart(fig_bubble, use_container_width=True)

else:
    st.info("👈 Silakan upload file 'Data Mahasiswa.csv' terlebih dahulu untuk meluncurkan dashboard analitik.")
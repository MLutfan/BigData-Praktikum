# =====================================
# REAL-TIME DASHBOARD (STREAMLIT)
# =====================================
import streamlit as st
import pandas as pd
import glob
import time
import os

st.set_page_config(
    page_title="Real-Time E-Commerce Dashboard",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Real-Time E-Commerce Dashboard")
st.markdown("*Streaming Batch Analytics - Big Data Technology*")
st.markdown("---")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "streaming", "output")

placeholder = st.empty()

def load_data():
    if not os.path.exists(OUTPUT_DIR):
        return pd.DataFrame(), f"Folder tidak ditemukan: {OUTPUT_DIR}"
        
    parquet_files = glob.glob(os.path.join(OUTPUT_DIR, "*.parquet"))
    
    if not parquet_files:
        return pd.DataFrame(), f"Menunggu data di folder: {OUTPUT_DIR}"
    
    df_list = []
    error_msg = ""
    
    for f in parquet_files:
        try:
            if os.path.getsize(f) > 0:
                df_temp = pd.read_parquet(f)
                if not df_temp.empty:
                    df_list.append(df_temp)
        except Exception as e:
            error_msg += f"Gagal membaca {os.path.basename(f)} | "

    if not df_list:
        return pd.DataFrame(), "Semua file parquet kosong atau sedang ditulis."
        
    try:
        df = pd.concat(df_list, ignore_index=True)
        
        # LOGIKA PINTAR: Cek apakah ini data mentah atau data agregasi
        if 'total_amount' in df.columns and 'quantity' in df.columns:
            # Jika data mentah, hitung (agregasi) sekarang juga!
            df_final = df.groupby(['city', 'product']).agg(
                revenue=('total_amount', 'sum'),
                total_items=('quantity', 'sum')
            ).reset_index()
        elif 'revenue' in df.columns and 'total_items' in df.columns:
            # Jika sudah diagregasi dari awal, gabungkan saja
            df_final = df.groupby(['city', 'product']).agg(
                revenue=('revenue', 'sum'),
                total_items=('total_items', 'sum')
            ).reset_index()
        else:
            return pd.DataFrame(), f"Format kolom tidak dikenali: {list(df.columns)}"
            
        return df_final, error_msg
    except Exception as e:
        return pd.DataFrame(), f"Error agregasi: {str(e)}"

# Loop Utama Dashboard
while True:
    df, status_msg = load_data()
    
    with placeholder.container():
        if df.empty:
            st.warning("⏳ Menunggu aliran data masuk...")
            st.info(f"Status: {status_msg}")
        else:
            if status_msg:
                st.warning(status_msg)
                
            # 1. Menghitung KPI Utama
            total_revenue = df['revenue'].sum()
            total_items = df['total_items'].sum()
            total_cities = df['city'].nunique()
            
            kpi1, kpi2, kpi3 = st.columns(3)
            kpi1.metric(label="Total Revenue", value=f"Rp {total_revenue:,.0f}")
            kpi2.metric(label="Total Items Sold", value=f"{total_items:,}")
            kpi3.metric(label="Cities Active", value=total_cities)
            
            st.markdown("---")
            
            # 2. Grafik Batang
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Top Revenue by City")
                city_revenue = df.groupby('city')['revenue'].sum().sort_values(ascending=False)
                st.bar_chart(city_revenue)
                
            with col2:
                st.subheader("Top Selling Products")
                product_qty = df.groupby('product')['total_items'].sum().sort_values(ascending=False)
                st.bar_chart(product_qty)
            
            st.markdown("---")
            
            # 3. Tabel Live
            st.subheader("Live Aggregated Data")
            formatted_df = df.sort_values('revenue', ascending=False).copy()
            st.dataframe(
                formatted_df.style.format({"revenue": "Rp {:,.0f}"}), 
                use_container_width=True,
                hide_index=True
            )
            
    time.sleep(3)
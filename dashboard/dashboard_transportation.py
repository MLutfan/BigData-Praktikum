import streamlit as st
import time
import sys
import os

# ==========================================
# FIX MODULE PATH
# ==========================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.analytics import transportation_analytics as ta
from scripts.alerts import transportation_alert as alert

# ==========================================
# CONFIG
# ==========================================
DATA_PATH = os.path.join(BASE_DIR, "data", "serving", "transportation")

st.set_page_config(
    page_title="Smart Transportation Dashboard",
    layout="wide"
)
# Judulnya kita perbarui untuk menandakan ini versi Praktikum 6
st.title("🚦 Smart Transportation Real-Time Analytics (Big Data Optimized)")

# AUTO REFRESH
REFRESH_INTERVAL = 5
placeholder = st.empty()

# ==========================================
# MAIN LOOP
# ==========================================
while True:
    with placeholder.container():
        # 1. LOAD DATA
        df = ta.load_data(DATA_PATH)
        
        if df.empty:
            st.warning("⏳ Waiting for streaming transportation data. Pastikan Terminal 1 & 2 berjalan...")
            time.sleep(REFRESH_INTERVAL)
            continue
            
        # 2. PREPROCESS
        df = ta.preprocess(df)
        
        # ==========================================
        # NEW PRAKTIKUM 6: OPTIMASI BIG DATA
        # Mengambil subset data untuk visualisasi agar tidak berat
        # ==========================================
        df_sample = df.tail(1000)
        
        # 3. METRICS (KPI Utama tetap menghitung dari seluruh data)
        try:
            metrics = ta.compute_metrics(df)
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Trips", metrics["total_trips"])
            col2.metric("Total Fare", f"Rp {int(metrics['total_fare']):,}")
            col3.metric("Top Location", metrics["top_location"])
        except Exception as e:
            st.error(f"Error computing metrics: {e}")
            
        st.divider()
        
        # 4. PEAK HOUR & ALERTS
        try:
            peak_hour = ta.detect_peak_hour(df)
            if peak_hour is not None:
                st.info(f"🕒 Peak traffic hour: {peak_hour}:00")
        except Exception:
            pass
            
        try:
            alerts = alert.generate_alert(df)
            if alerts:
                st.subheader("🚨 Traffic Alerts")
                for a in alerts:
                    st.error(a)
        except Exception as e:
            st.warning(f"Alert error: {e}")
            
        st.divider()
        
        # ==========================================
        # 5. VISUALISASI SKALA BESAR (NEW PRAKTIKUM 6)
        # ==========================================
        try:
            # Grafik agregasi per menit (sangat ringan)
            st.subheader("📈 Real-Time Traffic (Window Aggregation)")
            traffic_window = ta.traffic_per_window(df_sample)
            if traffic_window is not None:
                st.line_chart(traffic_window)
                
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("💰 Fare per Location")
                # Menggunakan df_sample (1000 data terakhir)
                st.bar_chart(ta.fare_per_location(df_sample))
            with col2:
                st.subheader("🚗 Vehicle Distribution")
                # Menggunakan df_sample (1000 data terakhir)
                st.bar_chart(ta.vehicle_distribution(df_sample))
                
            st.subheader("📈 Mobility Trend (Optimized)")
            # Menggunakan df_sample (1000 data terakhir)
            st.line_chart(ta.mobility_trend(df_sample))
        except Exception as e:
            st.warning(f"Visualization error: {e}")
            
        st.divider()
        
        # 6. ANOMALY (Mencari anomali dari sampel data)
        try:
            st.subheader("⚠️ Abnormal Trips")
            anomaly_df = ta.detect_anomaly(df_sample)
            if not anomaly_df.empty:
                st.dataframe(anomaly_df.tail(20), use_container_width=True)
            else:
                st.success("No anomalies detected")
        except Exception as e:
            st.warning(f"Anomaly error: {e}")
            
        st.divider()
        
        # 7. LIVE DATA (LIMITED VIEW)
        st.subheader("📋 Live Trip Data (Limited View)")
        # Hanya menampilkan 50 baris terbawah agar browser tidak lag
        st.dataframe(df_sample.tail(50), use_container_width=True)
        
    time.sleep(REFRESH_INTERVAL)
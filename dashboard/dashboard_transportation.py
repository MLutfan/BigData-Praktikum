import streamlit as st
import time
import sys
import os

# ==========================================
# FIX MODULE PATH
# ==========================================
# Daftarkan folder root (bigdata-project) ke dalam otak Python
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# IMPORT MODULE 
# (Pastikan nama file di sebelah kiri VS Code Anda persis sama dengan ini)
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
st.title("🚦 Smart Transportation Real-Time Analytics")

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
        
        # 3. METRICS
        try:
            metrics = ta.compute_metrics(df)
        except Exception as e:
            st.error(f"Error computing metrics: {e}")
            time.sleep(REFRESH_INTERVAL)
            continue
            
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Trips", metrics["total_trips"])
        col2.metric("Total Fare", f"Rp {int(metrics['total_fare']):,}")
        col3.metric("Top Location", metrics["top_location"])
        
        st.divider()
        
        # 4. PEAK HOUR
        try:
            peak_hour = ta.detect_peak_hour(df)
            if peak_hour is not None:
                st.info(f"🕒 Peak traffic hour: {peak_hour}:00")
        except Exception:
            st.warning("Tidak dapat menghitung peak hour")
            
        # 5. ALERTS
        try:
            alerts = alert.generate_alert(df)
            if alerts:
                st.subheader("🚨 Traffic Alerts")
                for a in alerts:
                    st.error(a)
        except Exception as e:
            st.warning(f"Alert error: {e}")
            
        st.divider()
        
        # 6. VISUALISASI
        try:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("💰 Fare per Location")
                st.bar_chart(ta.fare_per_location(df))
            with col2:
                st.subheader("🚗 Vehicle Distribution")
                st.bar_chart(ta.vehicle_distribution(df))
                
            st.subheader("📈 Mobility Trend")
            st.line_chart(ta.mobility_trend(df))
        except Exception as e:
            st.warning(f"Visualization error: {e}")
            
        st.divider()
        
        # 7. ANOMALY
        try:
            st.subheader("⚠️ Abnormal Trips")
            anomaly_df = ta.detect_anomaly(df)
            if not anomaly_df.empty:
                st.dataframe(anomaly_df.tail(20), use_container_width=True)
            else:
                st.success("No anomalies detected")
        except Exception as e:
            st.warning(f"Anomaly error: {e}")
            
        st.divider()
        
        # 8. LIVE DATA
        st.subheader("📋 Live Trip Data")
        st.dataframe(df.tail(50), use_container_width=True)
        
    time.sleep(REFRESH_INTERVAL)
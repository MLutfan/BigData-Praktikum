import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import os
import sys

# ==========================================
# FIX MODULE PATH (Mencegah Error di Windows)
# ==========================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Konfigurasi Path File
DATA_PATH = os.path.join(BASE_DIR, 'data', 'clean', 'traffic_smartcity_clean_v1.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'traffic_model_v1.pkl')

st.set_page_config(page_title="Smart Traffic AI", layout="wide")
st.title("🤖 Smart City Traffic AI Dashboard")

# ==========================================
# LOAD DATA & MODEL
# ==========================================
try:
    df = pd.read_csv(DATA_PATH)
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    st.error("Data atau Model tidak ditemukan. Pastikan Anda sudah menjalankan Data Cleaning dan ML Model.")
    st.stop()

# Feature Engineering ulang untuk menampilkan grafik historis
df['datetime'] = pd.to_datetime(df['datetime'])
df['hour'] = df['datetime'].dt.hour
df['day'] = df['datetime'].dt.dayofweek
df['lag1'] = df['traffic'].shift(1)
df = df.dropna()

# ==========================================
# 1. OVERVIEW METRICS
# ==========================================
st.subheader("📊 Statistik Historis Kemacetan")
col1, col2 = st.columns(2)
col1.metric("Avg Traffic (Rata-rata)", f"{int(df['traffic'].mean())} kendaraan")
col2.metric("Max Traffic (Puncak)", f"{int(df['traffic'].max())} kendaraan")

# ==========================================
# 2. GRAFIK TRAFFIC TREND
# ==========================================
st.subheader("📈 Traffic Trend (Historis)")
fig, ax = plt.subplots(figsize=(10, 3))
ax.plot(df['datetime'].tail(100), df['traffic'].tail(100).values, color='blue')
plt.xticks(rotation=45)
st.pyplot(fig)

st.divider()

# ==========================================
# 3. AI PREDICTION ENGINE
# ==========================================
st.subheader("🔮 Prediksi Kemacetan AI")
st.write("Silakan atur parameter di bawah ini untuk melihat prediksi kemacetan.")

col_a, col_b, col_c = st.columns(3)
with col_a:
    hour = st.slider("Pilih Jam (0-23)", 0, 23, 17) # Default jam 17 (5 sore)
with col_b:
    day = st.slider("Pilih Hari (0=Senin, 6=Minggu)", 0, 6, 2) # Default hari Rabu
with col_c:
    lag1 = st.number_input("Trafik 1 Jam Sebelumnya", 10, 500, 120)

if st.button("Jalankan Prediksi AI", type="primary"):
    # Memasukkan inputan pengguna ke dalam otak AI
    pred = model.predict([[hour, day, lag1]])
    
    # Menampilkan hasil
    pred_value = int(pred[0])
    if pred_value > 200:
        st.error(f"🚨 Awas Macet Parah! Prediksi: {pred_value} kendaraan")
    elif pred_value > 100:
        st.warning(f"⚠️ Ramai Lancar. Prediksi: {pred_value} kendaraan")
    else:
        st.success(f"✅ Jalanan Sepi. Prediksi: {pred_value} kendaraan")
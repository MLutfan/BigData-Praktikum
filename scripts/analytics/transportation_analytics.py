import pandas as pd
import os

# ==========================================
# LOAD DATA
# ==========================================
def load_data(path):
    if not os.path.exists(path):
        return pd.DataFrame()
    
    files = [f for f in os.listdir(path) if f.endswith(".parquet")]
    if not files:
        return pd.DataFrame()
        
    df = pd.concat(
        [pd.read_parquet(os.path.join(path, f)) for f in files],
        ignore_index=True
    )
    return df

# ==========================================
# PREPROCESS
# ==========================================
def preprocess(df):
    if df.empty:
        return df
    # Memperbaiki typo dari modul: ["timestamp") menjadi ["timestamp"]
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    # Memperbaiki typo dari modul: df df.dropna menjadi df = df.dropna
    df = df.dropna(subset=["timestamp"])
    return df

# ==========================================
# METRICS
# ==========================================
def compute_metrics(df):
    if df.empty:
        return {
            "total_trips": 0,
            "total_fare": 0,
            "top_location": "-"
        }
    return {
        "total_trips": len(df),
        "total_fare": df["fare"].sum(),
        "top_location": df.groupby("location")["fare"].sum().idxmax()
    }

# ==========================================
# PEAK HOUR
# ==========================================
def detect_peak_hour(df):
    if df.empty:
        return None
    df["hour"] = df["timestamp"].dt.hour
    return df.groupby("hour").size().idxmax()

# ==========================================
# VISUALIZATION DATA
# ==========================================
def fare_per_location(df):
    if df.empty:
        return pd.Series(dtype=float)
    return df.groupby("location")["fare"].sum().sort_values(ascending=False)

def vehicle_distribution(df):
    if df.empty:
        return pd.Series(dtype=float)
    return df.groupby("vehicle_type").size().sort_values(ascending=False)

def mobility_trend(df):
    if df.empty:
        return pd.Series(dtype=float)
    # Memperbaiki typo: df df.set_index menjadi df = df.set_index
    df = df.set_index("timestamp")
    # Memperbaiki typo: resample("105") menjadi resample("10S") yang artinya per 10 Detik
    return df["fare"].resample("10S").sum()

# ==========================================
# ANOMALY DETECTION
# ==========================================
def detect_anomaly(df):
    if df.empty:
        return pd.DataFrame()
    # Contoh: Tarif di atas Rp 80.000 dianggap anomali/mencurigakan
    return df[df["fare"] > 80000]

def traffic_per_window(df):
    if df.empty:
        return None
    # Pastikan kolom timestamp berformat datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    
    # Kelompokkan data per 1 menit dan hitung jumlah perjalanannya
    return df.set_index("timestamp").resample("1min").size()
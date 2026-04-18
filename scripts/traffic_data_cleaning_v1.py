import pandas as pd
import os

# Membuat folder clean secara otomatis jika belum ada
os.makedirs('data/clean', exist_ok=True)

print("Memulai Data Cleaning...")
# Membaca data mentah
df = pd.read_csv('data/raw/traffic_smartcity_v1.csv')

# Memperbaiki format waktu dan mengurutkannya
df['datetime'] = pd.to_datetime(df['datetime'])
df = df.sort_values('datetime')
df = df.dropna()

# Menyimpan data bersih
df.to_csv('data/clean/traffic_smartcity_clean_v1.csv', index=False)
print("Data cleaning selesai! Tersimpan di data/clean/traffic_smartcity_clean_v1.csv")
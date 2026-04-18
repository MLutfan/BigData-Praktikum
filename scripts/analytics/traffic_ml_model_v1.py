import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

# Membuat folder models secara otomatis jika belum ada
os.makedirs('models', exist_ok=True)

print("Melatih Model AI (Random Forest)...")
df = pd.read_csv('data/clean/traffic_smartcity_clean_v1.csv')

# Feature Engineering (Ekstraksi Jam, Hari, dan Data Sebelumnya)
df['datetime'] = pd.to_datetime(df['datetime'])
df['hour'] = df['datetime'].dt.hour
df['day'] = df['datetime'].dt.dayofweek
df['lag1'] = df['traffic'].shift(1)
df = df.dropna()

# Menentukan Input (X) dan Target Prediksi (y)
X = df[['hour', 'day', 'lag1']]
y = df['traffic']

# Membangun dan Melatih Model AI
model = RandomForestRegressor(random_state=42)
model.fit(X, y)

# Menyimpan 'Otak' AI yang sudah pintar ke format .pkl
joblib.dump(model, 'models/traffic_model_v1.pkl')
print("Model AI berhasil dipelajari dan disimpan di models/traffic_model_v1.pkl!")
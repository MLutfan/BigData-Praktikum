# 🚀 Big Data Analytics & Decision-Oriented System Pipeline

Repositori ini berisi implementasi *End-to-End Big Data Pipeline* yang mencakup *Batch Processing*, *Real-Time Streaming Analytics*, dan pembuatan *Decision-Oriented System Dashboard*. Proyek ini dikembangkan sebagai bagian dari praktikum mata kuliah **Big Data Technology** di **Program Studi Teknologi Informasi, UIN Antasari**.

## 📌 Deskripsi Proyek

Sistem ini mensimulasikan arsitektur Big Data modern (Lambda/Kappa Architecture) yang mampu memproses data mentah menjadi *actionable insights* secara *real-time*. Proyek ini dibagi menjadi dua domain studi kasus utama:

1. **E-Commerce Pipeline (Modul 1 - 4):**
   - Mensimulasikan data transaksi e-commerce.
   - Melakukan *batch processing* dan agregasi data untuk mengetahui metrik penjualan.
   - Mengimplementasikan *Streaming Processing* menggunakan Spark/Pandas untuk membaca data yang mengalir secara kontinu.
2. **Smart Transportation Pipeline (Modul 5):**
   - Mensimulasikan mobilitas kendaraan pintar (GPS/Lokasi, Tarif, Jarak).
   - Membangun **Decision-Oriented System** yang tidak hanya menampilkan data, tetapi juga menghasilkan peringatan otomatis (*Alerts*) untuk anomali seperti kemacetan atau tarif abnormal.

## 🛠️ Teknologi yang Digunakan

- **Bahasa Pemrograman:** Python 3
- **Data Processing Engine:** Apache Spark (PySpark) & Pandas
- **Storage / Data Lake:** Parquet (Columnar Storage), JSON
- **Real-Time Dashboard:** Streamlit
- **Version Control:** Git & GitHub

## 📂 Struktur Direktori

```text
BIGDATA-PROJECT/
├── dashboard/
│   ├── dashboard_streamlit.py           # Dashboard E-commerce (Modul 4)
│   └── dashboard_transportation.py      # Dashboard Smart Transportation (Modul 5)
├── data/
│   └── serving/
│       └── transportation/              # Parquet Data Lake (Hasil Streaming)
├── scripts/
│   ├── alerts/
│   │   ├── __init__.py
│   │   └── transportation_alert.py      # Logic untuk mendeteksi anomali & alert
│   ├── analytics/
│   │   ├── __init__.py
│   │   └── transportation_analytics.py  # Logic perhitungan metrik & agregasi
│   ├── transportation/
│   │   ├── trip_generator.py            # Simulator penghasil data JSON real-time
│   │   └── streaming_trip_layer.py      # Prosesor stream data (JSON -> Parquet)
│   └── stream_generator.py              # Generator E-Commerce
├── stream_data/
│   └── transportation/                  # Lokasi file JSON sementara sebelum diproses
├── .gitignore
└── README.md
```

⚙️ Cara Menjalankan Proyek (Smart Transportation)
Pastikan Python 3 sudah terinstal dan jalankan proyek ini di dalam Virtual Environment (venv).

1. Install Dependencies

```Bash
pip install pandas pyspark streamlit pyarrow
```
2. Jalankan Data Generator (Terminal 1)
Terminal ini akan bertindak sebagai pabrik data yang mensimulasikan perjalanan baru setiap 3 detik.

```Bash
python scripts/transportation/trip_generator.py
```
3. Jalankan Streaming Processor (Terminal 2)
Buka terminal baru. Script ini akan menangkap file JSON yang dihasilkan Generator, memprosesnya, dan menyimpannya ke Data Lake dalam format .parquet.

```Bash
python scripts/transportation/streaming_trip_layer.py
```
4. Jalankan Real-Time Dashboard (Terminal 3)
Buka terminal baru. Script ini akan membaca data dari Parquet dan merendernya ke dalam Dashboard web interaktif secara terus-menerus.

```Bash
python -m streamlit run dashboard/dashboard_transportation.py
```
📊 Fitur Dashboard (Modul 5)
- Live Metrics: Menampilkan Total Trips, Total Fare, dan Top Location.
- Decision Alerts: Deteksi otomatis volume traffic tinggi dan tarif abnormal.
- Visualisasi Dinamis: Bar chart distribusi kendaraan dan pendapatan per kota.
- Anomaly Detection: Tabel khusus yang menyaring trip dengan tarif yang mencurigakan.
- Live Data Feed: Tabel raw data yang terus diperbarui setiap 5 detik.

*Dibuat untuk memenuhi tugas praktikum Big Data Technology - 2026*

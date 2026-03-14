# =====================================
# STREAMING PROCESSOR (PANDAS BYPASS)
# =====================================
import pandas as pd
import os
import time
import glob

print("========================================")
print("     STREAMING PROCESSOR STARTED        ")
print("========================================")

INPUT_DIR = "data/streaming/input"
OUTPUT_DIR = "data/streaming/output"

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

processed_files = set()
batch_id = 0

try:
    while True:
        # Cari semua file JSON di folder input
        json_files = glob.glob(f"{INPUT_DIR}/*.json")
        new_files = [f for f in json_files if f not in processed_files]
        
        if new_files:
            print(f"\n--- Batch: {batch_id} ---")
            batch_data = []
            
            # Baca file JSON baru
            for file in new_files:
                try:
                    df_temp = pd.read_json(file, lines=True) if os.path.getsize(file) > 0 else pd.read_json(file, typ='series').to_frame().T
                    batch_data.append(df_temp)
                    processed_files.add(file)
                except Exception as e:
                    print(f"Skipping empty or invalid file: {file}")
            
            if batch_data:
                # Gabungkan data
                df_batch = pd.concat(batch_data, ignore_index=True)
                
                # Konversi tipe data waktu
                df_batch['timestamp'] = pd.to_datetime(df_batch['timestamp'])
                
                # Tampilkan hasil agregasi di terminal (seperti Spark)
                agg_df = df_batch.groupby(['city', 'product']).agg(
                    revenue=('total_amount', 'sum'),
                    total_items=('quantity', 'sum')
                ).reset_index()
                print(agg_df.to_string(index=False))
                
                # Simpan ke Parquet
                parquet_filename = f"{OUTPUT_DIR}/part-{batch_id:05d}.parquet"
                df_batch.to_parquet(parquet_filename, index=False)
                print(f"Saved to: {parquet_filename}")
                
            batch_id += 1
            
        time.sleep(3) # Cek file baru setiap 3 detik

except KeyboardInterrupt:
    print("\n========================================")
    print("     PROCESSOR STOPPED BY USER          ")
    print("========================================")
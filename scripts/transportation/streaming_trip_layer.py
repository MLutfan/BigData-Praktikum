import pandas as pd
import os
import time
import glob
import json

print("=== PANDAS STREAMING LAYER (BYPASS) STARTED ===")

INPUT_DIR = "stream_data/transportation"
OUTPUT_DIR = "data/serving/transportation"

# Otomatis membuat folder agar tidak error "Path not found"
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

processed_files = set()
batch_id = 0

try:
    while True:
        # Cari semua file JSON baru
        json_files = glob.glob(f"{INPUT_DIR}/*.json")
        new_files = [f for f in json_files if f not in processed_files]
        
        if new_files:
            print(f"\n--- Processing Batch: {batch_id} ---")
            batch_data = []
            
            # Baca file JSON satu per satu
            for file in new_files:
                try:
                    if os.path.getsize(file) > 0:
                        with open(file, 'r') as f:
                            data = json.load(f)
                            batch_data.append(pd.DataFrame([data]))
                    processed_files.add(file)
                except Exception as e:
                    print(f"Skipping file {file}: {e}")
            
            # Jika ada data, gabungkan dan simpan ke Parquet
            if batch_data:
                df_batch = pd.concat(batch_data, ignore_index=True)
                df_batch['timestamp'] = pd.to_datetime(df_batch['timestamp'])
                
                parquet_filename = f"{OUTPUT_DIR}/part-{batch_id:05d}.parquet"
                df_batch.to_parquet(parquet_filename, index=False)
                print(f"Saved {len(new_files)} trips to: {parquet_filename}")
                
            batch_id += 1
            
        time.sleep(3) # Cek file baru setiap 3 detik

except KeyboardInterrupt:
    print("\n=== STREAMING PROCESSOR STOPPED ===")
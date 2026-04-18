import json, time, random, os
from datetime import datetime

# Membuat folder output secara otomatis
OUTPUT_PATH = "stream_data/transportation"
os.makedirs(OUTPUT_PATH, exist_ok=True)

locations = ["Jakarta", "Bandung", "Surabaya"]
vehicles = ["Car", "Motorbike", "Taxi"]

i = 1
print(f"=== TRANSPORTATION GENERATOR STARTED ===")
print(f"Menyimpan data di: {OUTPUT_PATH}")

while True:
    data = {
        "trip_id": f"TRX{i}",
        "vehicle_type": random.choice(vehicles),
        "location": random.choice(locations),
        "distance": round(random.uniform(1, 20), 2),
        "fare": random.randint(10000, 100000),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Menyimpan data ke format JSON
    with open(f"{OUTPUT_PATH}/trip_{i}.json", "w") as f:
        json.dump(data, f)
        
    print("Generated Trip:", data)
    i += 1
    time.sleep(3) # Jeda 3 detik
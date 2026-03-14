# =====================================
# EVENT SIMULATOR (STREAM GENERATOR)
# =====================================
import json
import time
import random
import os
from datetime import datetime
import uuid

# Configuration
INPUT_DIR = "data/streaming/input"
os.makedirs(INPUT_DIR, exist_ok=True)

# Master Data
CITIES = ["Jakarta", "Surabaya", "Bandung", "Medan", "Bali"]
PRODUCTS = ["Laptop", "Smartphone", "Tablet", "Monitor", "Headphone"]
CATEGORIES = ["Electronics", "Electronics", "Electronics", "Accessories", "Accessories"]
PRICES = [15000000, 8000000, 5000000, 3000000, 1000000]

print("========================================")
print("     STREAMING GENERATOR STARTED        ")
print(f"     Target Directory: {INPUT_DIR}     ")
print("     Press Ctrl+C to stop               ")
print("========================================")

try:
    event_count = 0
    while True:
        # Generate random event data
        idx = random.randint(0, 4)
        event = {
            "event_id": str(uuid.uuid4()),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "customer_id": f"CUST-{random.randint(1000, 9999)}",
            "city": random.choice(CITIES),
            "product": PRODUCTS[idx],
            "category": CATEGORIES[idx],
            "price": PRICES[idx],
            "quantity": random.randint(1, 3)
        }
        
        # Calculate total amount
        event["total_amount"] = event["price"] * event["quantity"]

        # Write to JSON file
        filename = f"{INPUT_DIR}/event_{int(time.time())}_{event_count}.json"
        with open(filename, 'w') as f:
            json.dump(event, f)
            
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Generated: {event['product']} ({event['quantity']}x) - {event['city']}")
        
        event_count += 1
        time.sleep(3) # Wait 3 seconds before next event

except KeyboardInterrupt:
    print("\n========================================")
    print(f"     GENERATOR STOPPED BY USER         ")
    print(f"     Total Events Generated: {event_count}")
    print("========================================")
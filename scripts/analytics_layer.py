import pandas as pd
import os
import time

start_time = time.time()
print("========================================")
print("       ANALYTICS LAYER STARTED          ")
print("========================================")

# Buat folder serving
os.makedirs("data/serving/total_revenue", exist_ok=True)
os.makedirs("data/serving/top_products", exist_ok=True)
os.makedirs("data/serving/category_revenue", exist_ok=True)
os.makedirs("data/serving/avg_transaction", exist_ok=True)

print("Loading Clean Data...")
df = pd.read_csv("data/raw/ecommerce_raw.csv")

# ========================================================
# PERBAIKAN: Menghitung total_amount dari price * quantity
# ========================================================
df["total_amount"] = df["price"] * df["quantity"]

total_records = len(df)
print(f"Total Records: {total_records}")
print("----------------------------------------")

print("Calculating Total Revenue...")
total_revenue = pd.DataFrame([{"total_revenue": df["total_amount"].sum()}])
print(total_revenue.to_string(index=False))
total_revenue.to_csv("data/serving/total_revenue/part-00000.csv", index=False)
print("Total Revenue saved to data/serving/total_revenue")
print("----------------------------------------")

print("Calculating Top 10 Products...")
top_products = df.groupby("product")["quantity"].sum().reset_index().rename(columns={"quantity": "total_quantity"})
top_products = top_products.sort_values("total_quantity", ascending=False).head(10)
print(top_products.to_string(index=False))
top_products.to_csv("data/serving/top_products/part-00000.csv", index=False)
print("Top Products saved to data/serving/top_products")
print("----------------------------------------")

print("Calculating Revenue per Category...")
category_revenue = df.groupby("category")["total_amount"].sum().reset_index().rename(columns={"total_amount": "category_revenue"})
category_revenue = category_revenue.sort_values("category_revenue", ascending=False)
print(category_revenue.to_string(index=False))
category_revenue.to_csv("data/serving/category_revenue/part-00000.csv", index=False)
print("Category Revenue saved to data/serving/category_revenue")
print("----------------------------------------")

print("Calculating Average Transaction Value per Customer...")
avg_transaction = df.groupby("customer_id")["total_amount"].mean().reset_index().rename(columns={"total_amount": "avg_transaction_value"})
print(avg_transaction.head(5).to_string(index=False))
avg_transaction.to_csv("data/serving/avg_transaction/part-00000.csv", index=False)
print("Average Transaction saved to data/serving/avg_transaction")
print("----------------------------------------")

end_time = time.time()
execution_time = round(end_time - start_time, 2)
print("========================================")
print("   ANALYTICS LAYER COMPLETED SUCCESS    ")
print(f"   Execution Time: {execution_time} sec")
print("========================================")
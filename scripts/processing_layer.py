from pyspark.sql import SparkSession
import os

# Inisialisasi Spark
spark = SparkSession.builder \
    .appName("ProcessingLayer") \
    .master("local[*]") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# Pastikan folder tujuan tersedia
os.makedirs("data/clean/parquet", exist_ok=True)

# Membaca data raw (CSV)
print("1. Membaca data mentah dari data/raw/ecommerce_raw.csv...")
df_raw = spark.read.csv("data/raw/ecommerce_raw.csv", header=True, inferSchema=True)

# Menyimpan data bersih (Parquet)
print("2. Menyimpan data bersih ke format Parquet...")
df_raw.write.mode("overwrite").parquet("data/clean/parquet/")

print("=========================================")
print(" PROCESSING LAYER SELESAI!")
print(" Silakan cek folder data/clean/parquet/")
print("=========================================")
spark.stop()
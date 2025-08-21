# config.py
# Pusat semua variabel konfigurasi

import os
from dotenv import load_dotenv

load_dotenv()

# Konfigurasi Google Gemini
GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')
MODEL_NAME = 'gemini-1.5-pro-latest' # Atau model lain yang kamu gunakan

# Konfigurasi MinIO
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'localhost:9000')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
MINIO_BUCKET_NAME = 'putusan-pdf'

# Konfigurasi File & Proses
URL_FILENAME = 'urls.txt' # Nama file yang berisi daftar URL
OUTPUT_FILENAME_JSON = 'hasil_ekstraksi_putusan.json'
API_DELAY_SECONDS = 61 # Jeda antar request (15 detik = 4 request per menit, aman!)
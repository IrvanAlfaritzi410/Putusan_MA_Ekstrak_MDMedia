# config.py
# Pusat semua variabel konfigurasi

import os
from dotenv import load_dotenv

load_dotenv()

# Konfigurasi Google Gemini
MODEL_NAME = 'gemini-1.5-flash-latest'
GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')

# Konfigurasi MinIO
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'localhost:9000')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
MINIO_BUCKET_NAME = 'putusan-pdf'

# Konfigurasi File & Proses
URL_FILENAME = 'urls.txt' # Nama file yang berisi daftar URL
PDF_DOWNLOAD_FOLDER = 'downloaded_pdfs'
API_DELAY_SECONDS = 15 # Jeda antar request (15 detik = 4 request per menit, aman!)

# --- Konfigurasi MongoDB (BARU) ---
MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"
MONGO_DB_NAME = "db_putusan_ma"
MONGO_COLLECTION_NAME = "putusan"

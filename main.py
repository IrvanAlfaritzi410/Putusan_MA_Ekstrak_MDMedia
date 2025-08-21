# Library Standar Python
import os
import time

# Library Pihak Ketiga
import google.generativeai as genai
import boto3
from botocore.client import Config
from tqdm import tqdm
from pymongo import MongoClient # Import library MongoDB

# --- MENGHUBUNGKAN SEMUA MODUL ---
import config
from proses_URL import proses_putusan_from_url

# --- FUNGSI SETUP ---
def setup_model():
    # ... (Fungsi ini tidak berubah, tetap sama)
    if not config.GOOGLE_API_KEY:
        print("✗ Kunci API tidak tersedia di config.py atau .env file.")
        return None
    try:
        genai.configure(api_key=config.GOOGLE_API_KEY)
        model = genai.GenerativeModel(config.MODEL_NAME)
        print("✓ Konfigurasi Gemini API berhasil.")
        return model
    except Exception as e:
        print(f"✗ Konfigurasi API gagal: {e}")
        return None

def setup_s3_client():
    # ... (Fungsi ini tidak berubah, tetap sama)
    print("✓ Menyiapkan koneksi ke MinIO...")
    try:
        s3_client = boto3.client(
            's3',
            endpoint_url=f'http://{config.MINIO_ENDPOINT}',
            aws_access_key_id=config.MINIO_ACCESS_KEY,
            aws_secret_access_key=config.MINIO_SECRET_KEY,
            config=Config(signature_version='s3v4')
        )
        print("✓ Koneksi MinIO berhasil.")
        return s3_client
    except Exception as e:
        print(f"✗ Koneksi MinIO gagal: {e}")
        return None

def setup_mongo_client():
    """Mengkonfigurasi dan mengembalikan koneksi ke collection MongoDB."""
    print("✓ Menyiapkan koneksi ke MongoDB...")
    try:
        client = MongoClient(config.MONGO_CONNECTION_STRING)
        db = client[config.MONGO_DB_NAME]
        collection = db[config.MONGO_COLLECTION_NAME]
        # Test koneksi
        client.server_info() 
        print(f"✓ Koneksi MongoDB ke collection '{config.MONGO_COLLECTION_NAME}' berhasil.")
        return collection
    except Exception as e:
        print(f"✗ Koneksi MongoDB gagal: {e}")
        return None

# --- FUNGSI UTAMA (Dengan Logika MongoDB) ---
def main():
    """Fungsi utama untuk menjalankan seluruh pipeline ekstraksi."""
    model = setup_model()
    s3_client = setup_s3_client()
    mongo_collection = setup_mongo_client() # Setup koneksi MongoDB
    
    # PERBAIKAN: Mengubah cara pengecekan objek
    if model is None or s3_client is None or mongo_collection is None:
        print("Eksekusi dihentikan karena salah satu konfigurasi gagal.")
        return
    
    # Membaca daftar URL dari file eksternal
    try:
        with open(config.URL_FILENAME, 'r') as f:
            list_url_putusan = [line.strip() for line in f if line.strip()]
        print(f"✓ Berhasil memuat {len(list_url_putusan)} URL dari '{config.URL_FILENAME}'.")
    except FileNotFoundError:
        print(f"✗ Error: File '{config.URL_FILENAME}' tidak ditemukan.")
        return

    # Memuat URL yang sudah ada dari DATABASE untuk menghindari duplikasi
    processed_docs = mongo_collection.find({}, {"sumber_url": 1})
    processed_urls = {doc.get('sumber_url') for doc in processed_docs}
    urls_to_process = [url for url in list_url_putusan if url not in processed_urls]

    # Proses utama
    if not urls_to_process:
        print("\n✓ Semua URL sudah diproses sebelumnya dan ada di database.")
    else:
        print(f"\nMenemukan {len(urls_to_process)} URL baru untuk diproses.")
        for url in tqdm(urls_to_process, desc="Memproses URL", unit="url"):
            try:
                hasil = proses_putusan_from_url(model, s3_client, url)
                
                if hasil:
                    # LANGSUNG SIMPAN ke MongoDB
                    # Menggunakan update_one dengan upsert=True adalah cara paling aman
                    # Ini akan meng-update jika URL sudah ada, atau membuat data baru jika belum ada.
                    mongo_collection.update_one(
                        {'sumber_url': url},  # Filter untuk mencari dokumen
                        {'$set': hasil},      # Data yang akan dimasukkan/diperbarui
                        upsert=True           # Opsi untuk membuat data baru jika tidak ditemukan
                    )
                    tqdm.write(f"✓ Berhasil diekstrak dan disimpan ke MongoDB: {url}")
                
                time.sleep(config.API_DELAY_SECONDS)

            except Exception as e:
                tqdm.write(f"✗ Gagal memproses URL {url}: {e}")
                continue

    total_docs_in_db = mongo_collection.count_documents({})
    print(f"\n✓ Proses selesai. Total {total_docs_in_db} dokumen tersimpan di database MongoDB.")

# --- TITIK MASUK EKSEKUSI SKRIP ---
if __name__ == "__main__":
    main()

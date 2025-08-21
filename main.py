# main.py
# Skrip utama yang menjadi pusat kendali untuk menjalankan pipeline ekstraksi.

# Library Standar Python
import os
import json
import time

# Library Pihak Ketiga
import google.generativeai as genai
import boto3
from botocore.client import Config
from tqdm import tqdm # Import library progress bar

# --- MENGHUBUNGKAN SEMUA MODUL ---
# 1. Impor semua variabel konfigurasi dari file config.py
import config
# 2. Impor fungsi utama dari file proses_URL.py
from proses_URL import proses_putusan_from_url

# --- FUNGSI SETUP (Tidak ada perubahan, sudah bagus) ---
def setup_model():
    """Mengkonfigurasi dan mengembalikan model Gemini menggunakan variabel dari config."""
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
    """Mengkonfigurasi dan mengembalikan S3 client untuk MinIO."""
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

# --- FUNGSI UTAMA (Dengan Perbaikan) ---
def main():
    """Fungsi utama untuk menjalankan seluruh pipeline ekstraksi."""
    model = setup_model()
    s3_client = setup_s3_client()
    
    if not model or not s3_client:
        print("Eksekusi dihentikan karena konfigurasi gagal.")
        return
    
    # 1. Membaca daftar URL dari file eksternal
    try:
        with open(config.URL_FILENAME, 'r') as f:
            list_url_putusan = [line.strip() for line in f if line.strip()]
        print(f"✓ Berhasil memuat {len(list_url_putusan)} URL dari '{config.URL_FILENAME}'.")
    except FileNotFoundError:
        print(f"✗ Error: File '{config.URL_FILENAME}' tidak ditemukan.")
        return

    # 2. Memuat hasil yang sudah ada untuk menghindari duplikasi
    list_hasil_akhir = []
    if os.path.exists(config.OUTPUT_FILENAME_JSON):
        try:
            with open(config.OUTPUT_FILENAME_JSON, 'r', encoding='utf-8') as f:
                list_hasil_akhir = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            print(f"Warning: File output '{config.OUTPUT_FILENAME_JSON}' rusak atau tidak bisa dibaca. Memulai dengan list kosong.")
            list_hasil_akhir = []
            
    processed_urls = {item.get('sumber_url') for item in list_hasil_akhir}
    urls_to_process = [url for url in list_url_putusan if url not in processed_urls]

    # 3. Proses utama dengan progress bar dan penanganan error
    if not urls_to_process:
        print("\n✓ Semua URL sudah diproses sebelumnya.")
    else:
        print(f"\nMenemukan {len(urls_to_process)} URL baru untuk diproses.")
        # Menggunakan tqdm untuk progress bar yang interaktif
        for url in tqdm(urls_to_process, desc="Memproses URL", unit="url"):
            try:
                # Meneruskan objek 'model' dan 's3_client' ke dalam fungsi pemroses
                hasil = proses_putusan_from_url(model, s3_client, url)
                if hasil:
                    list_hasil_akhir.append(hasil)
                
                # Jeda antar request untuk menghindari limit API
                time.sleep(config.API_DELAY_SECONDS)

            except Exception as e:
                # Jika terjadi error pada satu URL, catat errornya dan lanjut ke URL berikutnya
                tqdm.write(f"✗ Gagal memproses URL {url}: {e}")
                continue

    # 4. Menyimpan hasil akhir
    if list_hasil_akhir:
        print(f"\nMenyimpan total {len(list_hasil_akhir)} data ke dalam file JSON...")
        with open(config.OUTPUT_FILENAME_JSON, 'w', encoding='utf-8') as f:
            json.dump(list_hasil_akhir, f, ensure_ascii=False, indent=4)
        print(f"✓ Data berhasil disimpan di '{config.OUTPUT_FILENAME_JSON}'")
    else:
        print("\nTidak ada data yang berhasil diekstrak atau semua sudah diproses.")

# --- TITIK MASUK EKSEKUSI SKRIP ---
if __name__ == "__main__":
    main()
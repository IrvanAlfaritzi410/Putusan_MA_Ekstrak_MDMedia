# Penerapan Metode Prompt Engineering Menggunakan Large Language Model (LLM) Google Gemini untuk Otomatisasi Ekstraksi Informasi Terstruktur Pada Dokumen Putusan Mahkamah Agung
Proyek ini merupakan sebuah pipeline data engineering yang dirancang untuk mengotomatisasi proses ekstraksi informasi terstruktur dari dokumen putusan Mahkamah Agung Republik Indonesia. Sistem ini mengubah dokumen PDF yang tidak terstruktur menjadi data JSON yang rapi dan siap untuk dianalisis, memanfaatkan kekuatan Large Language Model (LLM) Google Gemini.

Proyek ini dikembangkan sebagai bagian dari program Kerja Praktik di PT Metra Digital Media (MDMedia), departemen Digital Analysts.

# 🏛️ Arsitektur Sistem
<img width="940" height="443" alt="diagram-export-7-29-2025-3_07_39-PM(1)(1)" src="https://github.com/user-attachments/assets/1fd28a81-ed49-4b5c-908b-9b553dbb6a0e" />


Sistem ini bekerja dengan alur sebagai berikut:

1. Input: Proses dimulai dengan daftar URL halaman putusan yang disediakan dalam file urls.txt.

2. Scraping & Download: Skrip secara otomatis mengunjungi setiap URL, menemukan link unduhan PDF, dan mengunduhnya.

3. Penyimpanan Arsip: File PDF yang berhasil diunduh langsung diarsipkan ke dalam object storage MinIO untuk penyimpanan yang aman dan skalabel.

4. Ekstraksi Teks: Teks mentah diekstrak dari setiap file PDF menggunakan PyMuPDF.

5. Ekstraksi Cerdas dengan LLM: Teks mentah dikirim ke Google Gemini API dengan prompt yang dirancang khusus (prompt engineering) untuk mengekstrak informasi kunci.

6. Output: Hasil ekstraksi yang terstruktur disimpan secara inkremental ke dalam file JSON, siap untuk digunakan dalam analisis data lebih lanjut.

(Pastikan file flowchart_kp.png ada di dalam repositori agar gambar ini muncul)

# ✨ Fitur Utama
1. Otomatisasi End-to-End: Seluruh proses dari URL hingga JSON berjalan secara otomatis.

2. Ekstraksi Terstruktur: Menggunakan prompt engineering untuk mendapatkan data yang konsisten dan sesuai skema.

3. Penyimpanan Inkremental: Hasil disimpan satu per satu, memastikan tidak ada data yang hilang jika proses terganggu.

4. Penanganan Duplikasi: Skrip secara otomatis memeriksa URL yang sudah pernah diproses untuk menghindari pekerjaan ganda.

5. Arsip Dokumen: Menggunakan MinIO untuk menyimpan salinan asli dari setiap dokumen PDF yang diproses.

# 🛠️ Teknologi yang Digunakan
Bahasa Pemrograman: Python 3.11+

LLM: Google Gemini Pro

Ekstraksi Teks: PyMuPDF (fitz)

Web Scraping: requests, BeautifulSoup4

Object Storage: MinIO

Library Pendukung: python-dotenv, tqdm, boto3

# 🚀 Cara Menjalankan Proyek
1. Prasyarat
Python 3.11 atau lebih baru.

Docker Desktop terinstal dan berjalan.

Google Gemini API Key yang valid.

2. Setup Awal
a. Clone Repositori

git clone https://github.com/username/nama-repositori.git
cd nama-repositori

b. Jalankan MinIO via Docker
Buka terminal dan jalankan perintah berikut untuk memulai server MinIO.

docker run -p 9000:9000 -p 9001:9001 minio/minio server /data --console-address ":9001"

Akses dashboard MinIO di http://localhost:9001.

Login dengan kredensial default: minioadmin / minioadmin.

Buat sebuah bucket baru dengan nama putusan-pdf.

c. Instal Dependensi Python

pip install -r requirements.txt

d. Konfigurasi Environment
Buat sebuah file bernama .env di direktori utama proyek dan isi dengan kredensial Anda.

# Ganti dengan API Key Anda dari Google AI Studio
GOOGLE_API_KEY="AIzaSy...kunci_api_anda..."

# Kredensial untuk MinIO (sesuaikan jika Anda mengubahnya)
MINIO_ENDPOINT="localhost:9000"
MINIO_ACCESS_KEY="minioadmin"
MINIO_SECRET_KEY="minioadmin"

e. Siapkan Daftar URL
Buat file bernama urls.txt dan isi dengan daftar URL putusan yang ingin diproses, satu URL per baris.

https://putusan3.mahkamahagung.go.id/direktori/putusan/url-pertama.html
https://putusan3.mahkamahagung.go.id/direktori/putusan/url-kedua.html

3. Jalankan Skrip
Setelah semua setup selesai, jalankan skrip utama dari terminal:

python main.py

Proses akan berjalan dan hasilnya akan disimpan di hasil_ekstraksi_putusan.json.

# 📁 Struktur Proyek
.
├── .env              # Menyimpan kunci API dan kredensial (Jangan di-upload ke Git)
├── config.py         # Memuat semua variabel konfigurasi dari .env
├── extractor.py      # Berisi prompt dan fungsi untuk memanggil Gemini
├── main.py           # Skrip utama untuk menjalankan seluruh pipeline
├── proses_URL.py     # Logika untuk mengunduh PDF, menyimpan ke MinIO, dan ekstraksi teks
├── requirements.txt  # Daftar semua library Python yang dibutuhkan
└── urls.txt          # Daftar URL yang akan diproses

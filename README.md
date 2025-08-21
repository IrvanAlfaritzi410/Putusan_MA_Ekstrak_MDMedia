# Penerapan Metode Prompt Engineering Menggunakan Large Language Model (LLM) Google Gemini untuk Otomatisasi Ekstraksi Informasi Terstruktur Pada Dokumen Putusan Mahkamah Agung

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Google Gemini](https://img.shields.io/badge/LLM-Google%20Gemini-blueviolet.svg)](https://ai.google.dev/)
[![MinIO](https://img.shields.io/badge/Storage-MinIO-red.svg)](https://min.io/)
[![Requests](https://img.shields.io/badge/Library-Requests-orange.svg)](https://requests.readthedocs.io/en/latest/)
[![BeautifulSoup](https://img.shields.io/badge/Library-BeautifulSoup-green.svg)](https://www.crummy.com/software/BeautifulSoup/)
[![PyMuPDF](https://img.shields.io/badge/Library-PyMuPDF-yellow.svg)](https://pymupdf.readthedocs.io/en/latest/)

Proyek ini merupakan implementasi sistem otomatis untuk mengekstraksi informasi dari dokumen putusan Mahkamah Agung. Analisis ini memanfaatkan kemampuan **Large Language Model (LLM)**, yaitu **Google Gemini 1.5 Pro**, untuk mengklasifikasikan dan mengubah data tidak terstruktur (PDF) menjadi format JSON yang terstruktur dan siap pakai.

## ## Latar Belakang Proyek
Mengolah dokumen hukum secara manual sangat tidak efisien dan rentan terhadap kesalahan. Ulasan dan data dalam putusan pengadilan merupakan aset informasi yang berharga jika dapat diolah dengan benar. Proyek ini mencoba menjawab pertanyaan:
* Bagaimana cara mengotomatisasi ekstraksi data kunci dari ratusan dokumen putusan?
* Entitas penting apa saja yang bisa diekstrak secara konsisten (misal: nomor putusan, para pihak, amar putusan)?
* Bagaimana memastikan data yang diekstrak memiliki format yang seragam untuk analisis lebih lanjut?

## ## Fitur Utama
* **Otomatisasi Penuh**: Proses dari unduh PDF, arsip ke MinIO, hingga ekstraksi JSON berjalan otomatis.
* **Ekstraksi Cerdas**: Menggunakan Google Gemini untuk pemahaman konteks hukum.
* **Resume Capability**: Skrip dapat melanjutkan proses jika terhenti, tanpa mengulang dari awal.
* **Penyimpanan Terpusat**: Mengarsipkan semua dokumen PDF sumber ke object storage MinIO.

## ## Alur Kerja
<img width="940" height="443" alt="diagram-export-7-29-2025-3_07_39-PM(1)(1)" src="https://github.com/user-attachments/assets/54b85a43-749c-4be6-a901-3e7116bbb87b" />

1.  **Inisialisasi**: Skrip mengkonfigurasi koneksi ke Google Gemini API dan MinIO.
2.  **Baca URL**: Memuat daftar URL putusan dari `urls.txt`.
3.  **Proses per URL**:
    * Scraping halaman untuk menemukan link unduhan PDF.
    * Mengunduh dan menyimpan file PDF ke MinIO.
    * Mengekstrak teks mentah dari file PDF.
    * Mengirim teks ke Gemini API dengan *prompt* yang telah dirancang.
    * Menerima dan memvalidasi output JSON.
4.  **Simpan Hasil**: Menambahkan data JSON baru ke file `hasil_ekstraksi_putusan.json`.

## ## Instalasi
1.  **Kloning Repositori**
    ```bash
    git clone <url-repositori-anda>
    cd <nama-folder-proyek>
    ```
2.  **Buat & Aktifkan Lingkungan Virtual**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3.  **Instal Dependensi**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Konfigurasi `.env`**
    Buat file `.env` dan isi dengan kredensial Anda.
    ```env
    GOOGLE_API_KEY="AIzaSy...ANDA"
    MINIO_ENDPOINT="localhost:9000"
    MINIO_ACCESS_KEY="minioadmin"
    MINIO_SECRET_KEY="minioadmin"
    ```
5.  **Siapkan `urls.txt`**
    Isi file dengan daftar URL putusan yang akan diproses.

## ## Cara Menjalankan
```bash
python main.py

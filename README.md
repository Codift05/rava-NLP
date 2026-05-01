# Project NLP: Rava (Recap Voice Analysis Assistant)

![NLP](https://img.shields.io/badge/Domain-Natural%20Language%20Processing-blue.svg)
![Python](https://img.shields.io/badge/Language-Python-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**Rava** adalah sebuah aplikasi antarmuka desktop (*desktop application*) berbasis **Natural Language Processing (NLP)** yang dirancang untuk mengotomatisasi notulensi rapat. Aplikasi ini menangkap suara dari rapat secara langsung, mengubahnya menjadi teks (Speech-to-Text), lalu menyusun ringkasannya secara otomatis.

Proyek ini sangat cocok untuk memecahkan masalah umum pada rapat *online* seperti:
- Sulitnya mencatat seluruh percakapan secara manual.
- Kehilangan atau terlewatnya poin-poin penting.
- Tidak adanya dokumentasi otomatis yang dapat dibaca secara cepat.

---

## Fitur Utama

- **Audio Capture Sistem:** Mampu menangkap suara dari mikrofon maupun dari *speaker/loopback* sistem (suara peserta rapat lain).
- **Speech-to-Text Otomatis:** Menggunakan teknologi *Speech Recognition* berakurasi tinggi untuk mentranskripsi audio rapat menjadi teks.
- **Auto-Summarization:** Menggunakan model NLP berbasis Transformer untuk merangkum teks yang panjang menjadi ringkasan yang padat dan inti.
- **Antarmuka (GUI) Responsif:** Aplikasi dibangun menggunakan PyQt6 yang modern. Pemrosesan *Machine Learning* dilakukan secara *asynchronous* (di latar belakang) sehingga aplikasi tidak akan macet (freeze).

---

## Arsitektur & Teknologi NLP

Proyek ini mengandalkan dua pilar utama dalam ranah AI / NLP:

1. **Automatic Speech Recognition (ASR):**
   - Menggunakan model **Whisper** dari OpenAI.
   - Digunakan untuk mengubah representasi akustik (audio) menjadi representasi linguistik (teks transkripsi).
   
2. **Abstractive Text Summarization:**
   - Menggunakan ekosistem **Hugging Face Transformers**.
   - Model diset secara default untuk menangani bahasa (misalnya: `cahya/bert2bert-indonesian-summarization` untuk bahasa Indonesia atau `facebook/bart-large-cnn` untuk bahasa Inggris).
   - Berguna untuk menangkap konteks pembicaraan dan merangkumnya secara kohesif.

### Teknologi Pendukung Lainnya:
- **Bahasa Pemrograman:** Python 3
- **Audio Processing:** `sounddevice`, `numpy`, `scipy`
- **UI Framework:** `PyQt6`

---

## Struktur Direktori Proyek

```text
Project_NLP/
│
├── app.py                # File utama untuk menjalankan aplikasi (GUI dengan PyQt6)
├── audio_capture.py      # Modul perekaman suara (Sounddevice & Queue)
├── stt_engine.py         # Modul NLP: Speech-to-Text menggunakan Whisper
├── summarizer.py         # Modul NLP: Summarization menggunakan HuggingFace Transformers
├── requirements.txt      # Daftar dependensi Python
└── README.md             # Dokumentasi utama proyek
```

---

## Panduan Instalasi & Menjalankan Aplikasi

Karena ini adalah proyek *Machine Learning*, instalasi akan mengunduh model AI yang berukuran cukup besar (seperti PyTorch).

### 1. Persiapan Environment
Buka terminal dan navigasikan ke direktori proyek ini.
```bash
# Membuat Virtual Environment
python3 -m venv venv

# Mengaktifkan Virtual Environment
source venv/bin/activate
```

### 2. Instalasi Dependensi
Jalankan perintah berikut untuk menginstal semua pustaka NLP dan UI:
```bash
pip install -r requirements.txt
```
*(Catatan: Proses ini mungkin memakan waktu lama karena akan mengunduh `torch` dan pustaka CUDA yang ukurannya bisa lebih dari 1GB).*

### 3. Menjalankan Aplikasi
Pastikan *Virtual Environment* sudah aktif, kemudian jalankan:
```bash
python app.py
```

---

## Menggunakan Aplikasi (Cara Kerja)

1. **Pilih Input Device:** Saat aplikasi terbuka, pilih perangkat input audio Anda dari menu *dropdown*. (Untuk menangkap suara rapat dari Google Meet/Zoom, pilih device bertipe *Monitor* atau *Loopback*).
2. **Mulai Rekaman:** Klik tombol **"Start Recording"** saat rapat dimulai.
3. **Selesai & Proses:** Klik **"Stop & Process"** saat rapat berakhir.
4. **Pemrosesan NLP:** Rava akan secara otomatis menjalankan model STT (Whisper) untuk menghasilkan **Transcription**, dan model NLP (Transformers) untuk menghasilkan **Summary**. Hasil akan langsung ditampilkan di layar Anda!

---

## Rencana Pengembangan (Roadmap)

- [ ] **Speaker Diarization:** Menambahkan NLP untuk mengidentifikasi "Siapa berbicara apa" (Speaker Identification).
- [ ] **Real-time Transcription:** Mengubah STT dari pemrosesan batch ke pemrosesan *streaming real-time*.
- [ ] **Ekspor Dokumen:** Menyediakan opsi untuk mengekspor hasil rapat ke PDF atau Word (`.docx`).

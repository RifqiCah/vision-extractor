# SmartBoard AI

Aplikasi berbasis Computer Vision untuk mengubah foto papan tulis atau catatan fisik menjadi aset digital yang terstruktur.

## Fitur Utama

### Digitize Notes
Mengubah tulisan tangan dari foto menjadi dokumen teks Markdown yang rapi. AI akan memperbaiki struktur kalimat dan format agar mudah dibaca.

### Action Items Extraction
Menganalisis konten catatan meeting atau kuliah untuk mendeteksi poin-poin tugas (Task), Penanggung Jawab (PIC), dan Tenggat Waktu (Deadline) secara otomatis dalam format JSON terstruktur.

## Tech Stack

* **Python 3.10**
* **Streamlit** (User Interface)
* **Google Gemini 1.5 Flash** (Multimodal LLM)

## Cara Menjalankan

1.  **Clone Repository**
    ```bash
    git clone [https://github.com/RifqiCah/vision-extractor.git](https://github.com/RifqiCah/vision-extractor.git)
    cd vision-extractor
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup API Key**
    Buat file `.env` dan masukkan API Key Google Gemini:
    ```env
    GOOGLE_API_KEY=Paste_API_Key_Disini
    ```

4.  **Jalankan Aplikasi**
    ```bash
    streamlit run app.py
    ```

## Struktur Project

```text
vision-extractor/
├── app.py                # Interface Utama
├── services/             # Logika AI (Gemini)
├── config/               # Konfigurasi Environment
└── utils/                # Helper Functions
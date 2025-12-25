import google.generativeai as genai
from config.settings import settings
import json

class VisionAnalyzer:
    def __init__(self):
        settings.validate()
        genai.configure(api_key=settings.API_KEY)
        self.model = genai.GenerativeModel(settings.MODEL_NAME)

    def digitize_notes(self, image):
        """
        Mengubah tulisan tangan/papan tulis menjadi catatan digital rapi.
        """
        prompt = """
        Kamu adalah asisten notulen profesional. 
        Tugasmu:
        1. BACA semua tulisan tangan atau diagram di papan tulis/kertas ini.
        2. UBAH menjadi format Markdown yang sangat rapi dan terstruktur.
        3. PERBAIKI kalimat yang tidak lengkap atau singkatan agar enak dibaca.
        4. JIKA ada diagram, jelaskan alur diagram tersebut dalam bentuk poin-poin.
        
        Output harus langsung berupa teks Markdown (Headings, Bullet points).
        """
        try:
            response = self.model.generate_content([prompt, image])
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

    def extract_action_items(self, image):
        """
        Mencari tugas/PR/Deadline dari foto papan tulis.
        """
        prompt = """
        Analisis foto papan tulis/catatan meeting ini.
        Cari dan ekstrak informasi berikut dalam format JSON:
        {
            "topic": "Topik Utama Pembahasan",
            "summary": "Ringkasan singkat 1 paragraf",
            "action_items": [
                {"task": "Apa yang harus dikerjakan", "assignee": "Siapa yang mengerjakan (jika ada)", "deadline": "Kapan (jika ada)"}
            ],
            "key_decisions": ["Keputusan penting yang disepakati"]
        }
        Jika tidak ada tanggal/orang spesifik, kosongkan atau isi null.
        Keluarkan JSON murni.
        """
        try:
            response = self.model.generate_content([prompt, image])
            return response.text.strip()
        except Exception as e:
            return json.dumps({"error": str(e)})
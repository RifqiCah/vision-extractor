import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    API_KEY = os.getenv("GOOGLE_API_KEY")
    # Menggunakan model Flash karena cepat & gratis tier, tapi jago vision
    MODEL_NAME = "gemini-2.5-flash" 

    @staticmethod
    def validate():
        if not Settings.API_KEY:
            raise ValueError("❌ CRITICAL: API Key belum diisi di file .env!")

settings = Settings()
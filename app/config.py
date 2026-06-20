import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "RAG Document Ingestion"
    API_V1_STR: str = "/api/v1"
    
    # Uploads directory setup
    UPLOAD_DIR: str = "uploads"
    BASE_URL: str = "http://127.0.0.1:8000"

    class Config:
        env_file = ".env"

settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
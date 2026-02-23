import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import Optional
load_dotenv()

class Settings(BaseSettings):
    avatar_path: str = "avatars/default"
    output_path: str = "outputs"
    class Config:
        pass
    APP_NAME: str = "AI Avatar System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WS_PORT: int = 8765

    DATABASE_URL: str = "sqlite:///./avatars.db"
    REDIS_URL: str = "redis://localhost:6379"
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    

    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    AVATAR_DIR: str = os.path.join(BASE_DIR, "avatars")
    OUTPUT_DIR: str = os.path.join(BASE_DIR, "outputs")
    STATIC_DIR: str = os.path.join(BASE_DIR, "static")
    

    AVATAR_MODELS: list = ["professional", "casual", "friendly", "corporate"]
    DEFAULT_AVATAR: str = "professional/model_v1"
    
    VIDEO_FPS: int = 30
    VIDEO_WIDTH: int = 1920
    VIDEO_HEIGHT: int = 1080
    VIDEO_CODEC: str = "h264"
    VIDEO_BITRATE: str = "5000k"
    AUDIO_SAMPLE_RATE: int = 16000
    AUDIO_CHANNELS: int = 1
    AUDIO_CODEC: str = "aac"
    STT_ENGINE: str = "google"  
    TTS_ENGINE: str = "azure"  
    AZURE_SPEECH_KEY: Optional[str] = None
    AZURE_SPEECH_REGION: Optional[str] = None
    ELEVENLABS_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    LLM_ENDPOINT: str = "http://localhost:8080/generate"
    LLM_API_KEY: Optional[str] = None
    CACHE_TTL: int = 3600
    ENABLE_CACHE: bool = True
    RTC_ICE_SERVERS: list = [
        {"urls": ["stun:stun.l.google.com:19302"]},
        {"urls": ["stun:stun1.l.google.com:19302"]}
    ]
    
    class Config:
        env_file = ".env"
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create directories
        os.makedirs(self.AVATAR_DIR, exist_ok=True)
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)
        os.makedirs(self.STATIC_DIR, exist_ok=True)

settings = Settings()

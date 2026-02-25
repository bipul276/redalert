import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "RedAlert Hub"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "")
    
    # Database
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'redalert_v4.db')}")

    class Config:
        case_sensitive = True

settings = Settings()

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "RedAlert Hub"
    API_V1_STR: str = "/api/v1"
    
    # Database
    # Ensure DB is always in the project root, regardless of where the app is run from
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # Database
    # Ensure DB is always in the project root, regardless of where the app is run from
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # Priority: Env Var (Prod) -> SQLite File (Local)
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'redalert_v3.db')}")
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "redalert_hub"


    class Config:
        case_sensitive = True

settings = Settings()

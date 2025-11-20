import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://user:pass@localhost/asili_ssms")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # M-Pesa
    MPESA_CONSUMER_KEY: str = os.getenv("MPESA_CONSUMER_KEY")
    MPESA_CONSUMER_SECRET: str = os.getenv("MPESA_CONSUMER_SECRET")
    MPESA_SHORTCODE: str = os.getenv("MPESA_SHORTCODE")
    
    # Security
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "https://asili.education.ke"]
    
    class Config:
        env_file = ".env"

settings = Settings()
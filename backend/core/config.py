from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Resume Annotation Tool"
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "DATABASE_URL", "sqlite:///./sql_app.db"
    )
    
    # 文件存储配置
    UPLOAD_DIR: str = "uploads"
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS: set = {"pdf", "json"}
    
    # 安全配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    class Config:
        case_sensitive = True

settings = Settings() 
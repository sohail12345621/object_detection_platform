from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Object Detection & Tracking Platform"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    
    # Paths
    UPLOAD_DIR: str = "../uploads"
    OUTPUT_DIR: str = "../outputs"
    WEIGHTS_DIR: str = "../weights"
    
    # Model
    DEFAULT_MODEL: str = "yolov8n.pt"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

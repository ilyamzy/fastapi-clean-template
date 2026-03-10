from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    FIREBASE_CREDENTIALS_PATH: str
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    FIREBASE_CREDENTIALS_PATH: str
    BASE_URL: str
    S3_ENDPOINT: str
    S3_BUCKET: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_REGION: str
    CACHE_DIR: str
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()

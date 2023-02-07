from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    DB_IP: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str
    REDIS_IP: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


config = Settings()

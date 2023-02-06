from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    DATABASE_IP: str
    REDIS_IP: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


config = Settings()

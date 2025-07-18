import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TOKEN: str
    SUPER_ADMIN_ID: int
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )

    def get_db_url(self) -> str:
        f''' 
            Возвращает адрес базы данных который собирается на основе .env
        '''

        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

        
settings = Settings()
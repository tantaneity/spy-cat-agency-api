from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    cat_api_url: str

    class Config:
        env_file = ".env"

settings = Settings()

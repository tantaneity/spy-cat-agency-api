from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://spycat:spycat@localhost:5432/spycatdb"
    cat_api_url: str = "https://api.thecatapi.com/v1/breeds"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_uri: str
    mongo_db_name: str = "notely"
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "mistral"

    class Config:
        env_file = ".env"


settings = Settings()

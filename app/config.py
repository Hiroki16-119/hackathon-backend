from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "FastAPI-Firuda"
    app_env: str = "development"
    app_port: int = 8000
    frontend_origin: str = "http://localhost:5173"

    class Config:
        env_file = ".env"

settings = Settings()

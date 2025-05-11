from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    livekit_api_key: str = ""
    livekit_api_secret: str = ""
    livekit_host: str = "http://localhost:7880"
    
    class Config:
        env_file = ".env"

settings = Settings()
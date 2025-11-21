from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    orion_can_channel: str = "can0"
    orion_can_bustype: str = "socketcan"
    orion_can_bitrate: int = 500_000

    class Config:
        env_file = ".env"


settings = Settings()

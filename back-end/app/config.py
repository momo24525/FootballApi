from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    request_timeout_seconds: float = 10.0

    class Config:
        env_file = ".env"


settings = Settings() # type: ignore
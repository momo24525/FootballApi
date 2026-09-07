from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bigballs_base_url: str = "https://api.bigballsdata.com"
    bigballs_api_key: str
    request_timeout_seconds: float = 10.0

    class Config:
        env_file = ".env"


settings = Settings() # type: ignore
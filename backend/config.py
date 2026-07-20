from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # No default here on purpose: if .env / env vars are missing, the app
    # should fail to start rather than silently sign tokens with a key
    # that's sitting in source control.
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()

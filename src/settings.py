from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_SERVER: str
    DB_NAME: str

    REDDIT_CLIENT_ID: str
    REDDIT_CLIENT_SECRET: str
    REDDIT_USERNAME: str
    REDDIT_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASSWORD: str
    REDIS_DB: str

    COINMARKETCAP_API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()

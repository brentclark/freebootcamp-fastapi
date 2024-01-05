from typing import Any
from pydantic_settings import BaseSettings
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(".env"))


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECRET_KEY: str
    ALGORITHM: str
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_HOST: str
    MYSQL_PASSWORD: str
    MYSQL_RANDOM_ROOT_PASSWORD: str


settings: Any = Settings()
# config: str = Config(".env")

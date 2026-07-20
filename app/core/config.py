from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_host: str = 'localhost'
    db_port: int = 5432
    db_user: str = 'postgres'
    db_password: str = 'postgres'
    db_name: str = 'fastapi_db'
    secret_key: str = 'secret_key'
    algorithm: str = 'HS256'

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


@lru_cache
def get_settings() ->Settings:
    return Settings()


settings = get_settings()


@lru_cache
def get_auth_data():
    return {'secret_key': settings.secret_key, 'algorithm': settings.algorithm}

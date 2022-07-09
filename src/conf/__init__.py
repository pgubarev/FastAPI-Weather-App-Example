__all__ = ('settings', 'api_config')


from pydantic import BaseSettings

from . import api_config


class ProjectSettings(BaseSettings):
    SECRET_KEY: str
    JWT_SECRET: str
    DATABASE_URL: str
    REDIS_URL: str
    OPEN_WEATHER_API_KEY: str


settings = ProjectSettings(_env_file='.env', _env_file_encoding='utf-8')

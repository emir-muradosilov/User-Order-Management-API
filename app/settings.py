from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class DatabaseConfig(ConfigBase):


    db_user:str = Field(env='DB_USER')
    db_pass:str = Field(env='DB_PASS')
    db_host:str = Field(env='DB_HOST')
    db_port:str = Field(env='DB_PORT')
    db_name:str = Field(env='DB_NAME')

class Config(BaseSettings):
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)


    @classmethod
    def load(cls) -> "Config":
        return cls()

config = Config.load()


REFRESH_COOKIE_NAME = "refresh_token"
REFRESH_COOKIE_PATH = "/api/v1/auth"
REFRESH_COOKIE_SECURE = False  # True в проде (HTTPS)
REFRESH_COOKIE_SAMESITE = "lax"

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class DatabaseConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="db_")

    db_user:str
    db_pass:str
    db_host:str
    db_port:str
    db_name:str

class Config(BaseSettings):
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)


    @classmethod
    def load(cls) -> "Config":
        return cls()

config = Config.load()

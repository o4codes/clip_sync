from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    secret_key: str
    debug: bool
    version: str = Field(default="v1")
    hash_scheme: str
    token_algorithm: str
    access_token_expire_minutes: int

    # DATABASE VARS
    db_uri: str
    db_name: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
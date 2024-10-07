from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import DirectoryPath, validator
from pydantic_settings import BaseSettings
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    DB_CONNECTION: Optional[str]
    DB_HOST: Optional[str]
    DB_PORT: Optional[str]
    DB_DATABASE: Optional[str]
    DB_USERNAME: Optional[str]
    DB_PASSWORD: Optional[str]
    SQLALCHEMY_DATABASE_URL: str = ""

    @validator("SQLALCHEMY_DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str) and v:
            return v
        if not (connection := values.get("DB_CONNECTION")):
            raise ValueError(
                "must specify at least DB_CONNECTION or SQLALCHEMY_DATABASE_URL",
            )
        username = values.get("DB_USERNAME")
        password = values.get("DB_PASSWORD")
        host = values.get("DB_HOST")
        port = values.get("DB_PORT")
        database = values.get("DB_DATABASE")

        return URL(
            drivername=f"{connection}+pymysql",
            username=username,
            password=password,
            host=host,
            port=int(port) if port else None,
            database=database,
            query=[],
        ).render_as_string(hide_password=False)

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

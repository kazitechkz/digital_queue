from typing import Optional
from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

# Загружаем данные с .env
load_dotenv()


class AppConfiguration(BaseSettings):
    # App Basic Settings
    app_name: str = Field(default="Цифровая очередь АКТЗФ", env="APP_NAME")
    app_description: str = Field(
        default="Сервис электронной очереди", env="APP_DESCRIPTION"
    )
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    app_debug: bool = Field(default=False, env="APP_DEBUG")
    app_docs_url: Optional[str] = Field(default=False, env="APP_DOCS_URL")
    app_redoc_url: Optional[str] = Field(default=False, env="APP_REDOC_URL")
    app_status: str = Field(default="development", env="APP_STATUS")
    # Database Choice: 'postgresql' or 'mysql'
    app_database: Optional[str] = Field(default="postgresql", env="APP_DATABASE")
    # Database Settings
    db_pool_size: int = Field(..., env="DB_POOL_SIZE")
    db_max_overflow: int = Field(..., env="DB_MAX_OVERFLOW")
    db_pool_timeout: int = Field(..., env="DB_POOL_TIMEOUT")
    db_pool_recycle: int = Field(..., env="DB_POOL_RECYCLE")
    # My SQL
    mysql_connection: str = Field(default="mysql+aiomysql", env="MYSQL_CONNECTION")
    mysql_db_host: str = Field(default="localhost", env="MYSQL_DB_HOST")
    mysql_db_port: int = Field(default=5432, env="MYSQL_DB_PORT")
    mysql_db_user: str = Field(default="postgres", env="MYSQL_DB_USER")
    mysql_db_password: str = Field(default="root", env="MYSQL_DB_PASSWORD")
    mysql_db_name: str = Field(default="digital_queue", env="MYSQL_DB_NAME")
    # PostgreSQL specific settings
    pg_connection: str = Field(default="postgresql+asyncpg", env="PG_CONNECTION")
    pg_db_host: str = Field(default="localhost", env="PG_DB_HOST")
    pg_db_port: int = Field(default=5432, env="PG_DB_PORT")
    pg_db_user: str = Field(default="postgres", env="PG_DB_USER")
    pg_db_password: str = Field(default="root", env="PG_DB_PASSWORD")
    pg_db_name: str = Field(default="digital_queue", env="PG_DB_NAME")
    # Authentication
    app_auth_type: str = Field(..., env="APP_AUTH_TYPE")
    # Local Authorization
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(..., env="ALGORITHM")
    access_token_expire_minutes: int = Field(..., env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(..., env="REFRESH_TOKEN_EXPIRE_DAYS")
    # Keycloak Authorization
    keycloak_server_url: str = Field(..., env="KEYCLOAK_SERVER_URL")
    keycloak_realm: str = Field(..., env="KEYCLOAK_REALM")
    keycloak_client_id: str = Field(..., env="KEYCLOAK_CLIENT_ID")
    keycloak_client_secret: str = Field(..., env="KEYCLOAK_CLIENT_SECRET")

    @property
    def get_connection_url(self) -> str:
        """Get the connection URL for the chosen database."""
        if self.app_database == "postgresql":
            return f"{self.pg_connection}://{self.pg_db_user}:{self.pg_db_password}@{self.pg_db_host}:{self.pg_db_port}/{self.pg_db_name}"
        elif self.app_database == "mysql":
            return f"{self.mysql_connection}://{self.mysql_db_user}:{self.mysql_db_password}@{self.mysql_db_host}:{self.mysql_db_port}/{self.mysql_db_name}"
        else:
            raise ValueError("Неверная строка подключения")

    @field_validator("app_status")
    def validate_app_status(cls, v):
        if v.lower() not in {"development", "production"}:
            raise ValueError("APP_STATUS должен быть 'development' или 'production'")
        return v

    @field_validator("app_auth_type")
    def validate_app_auth_type(cls, v):
        if v.lower() not in {"local", "keycloak"}:
            raise ValueError("APP_AUTH_TYPE должен быть 'local' или 'keycloak'")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Загрузка конфигурации из.env-файла и создание экземпляра конфигурации
app_config = AppConfiguration()

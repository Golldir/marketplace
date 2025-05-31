from zoneinfo import ZoneInfo

from dynaconf import Dynaconf
from pydantic import AnyUrl, BaseModel, AmqpDsn
from pydantic_settings import BaseSettings
import os

config_file = os.getenv("APP_ENV", "dev")

_settings = Dynaconf(settings_files=[f"config.{config_file}.yaml"]) 
_project_timezone = "Europe/Moscow"

_db_dsn = AnyUrl.build(
    scheme="postgresql+asyncpg",
    username=_settings.database.user,
    password=str(_settings.database.password),
    host=_settings.database.host,
    port=_settings.database.port,
    path=_settings.database.db,
)

_rabbit_url = AmqpDsn.build(
    scheme="amqp",
    host=_settings.rabbitmq.host,
    port=_settings.rabbitmq.port,
    username=_settings.rabbitmq.user,
    password=_settings.rabbitmq.password,
)

class S3Settings(BaseModel):
    access_key: str
    secret_key: str
    region: str
    endpoint: str
    bucket: str

class AuthSettings(BaseModel):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

class RabbitMQSettings(BaseModel):
    host: str
    port: int
    user: str
    password: str

class SMTPSettings(BaseModel):
    host: str
    port: int
    user: str
    password: str

class Settings(BaseSettings):
    app_name: str
    timezone: str
    tz: ZoneInfo
    app_env: str
    db_dsn: str
    first_external_host: str
    second_external_host: str
    s3: S3Settings
    auth: AuthSettings
    rabbitmq: str
    smtp: SMTPSettings

settings = Settings(
    app_name="example_api",
    timezone=_project_timezone,
    tz=ZoneInfo(_project_timezone),
    app_env=_settings.app_env,
    db_dsn=str(_db_dsn),
    first_external_host=_settings.first_external_host,
    second_external_host=_settings.second_external_host,

    s3=S3Settings(
        access_key=_settings.s3.access_key,
        secret_key=_settings.s3.secret_key,
        region=_settings.s3.region,
        endpoint=_settings.s3.endpoint,
        bucket=_settings.s3.bucket,
    ),
    auth=AuthSettings(
        SECRET_KEY=_settings.auth.SECRET_KEY,
        ALGORITHM=_settings.auth.ALGORITHM,
        ACCESS_TOKEN_EXPIRE_MINUTES=_settings.auth.ACCESS_TOKEN_EXPIRE_MINUTES
    ),
    rabbitmq=str(_rabbit_url),
    
    smtp=SMTPSettings(
        host=_settings.smtp.host,
        port=_settings.smtp.port,
        user=_settings.smtp.user,
        password=_settings.smtp.password
    )
)
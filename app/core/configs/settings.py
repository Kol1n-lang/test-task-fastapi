from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    host: str = Field(alias="DB_HOST", default="localhost")
    port: int = Field(alias="DB_PORT", default=5432)
    user: str = Field(alias="DB_USER", default="postgres")
    password: str = Field(alias="DB_PASSWORD", default="your-password")
    db: str = Field(alias="DB_NAME", default="your-database")

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class JWTSettings(BaseSettings):
    access_token_expire_minutes: int = Field(
        alias="ACCESS_TOKEN_EXPIRE_MINUTES", default=60
    )
    refresh_token_expire_minutes: int = Field(
        alias="REFRESH_TOKEN_EXPIRE_MINUTES", default=30
    )
    secret_key: str = Field(alias="SECRET_KEY", default="your-secret-key")
    algorithm: str = Field(alias="ALGORITHM", default="your-algorithm")


class ExternalSettings(BaseSettings):
    api_secret_key: str = Field(alias="API_SECRET_KEY", default="your-api-secret-key")
    email_sender: str = Field(alias="EMAIL_SENDER", default="your-email-sender")
    app_password: str = Field(alias="APP_PASSWORD", default="your-app-password")


class RedisSettings(BaseSettings):
    host: str = Field(alias="REDIS_HOST", default="localhost")
    port: int = Field(alias="REDIS_PORT", default=6379)
    db: int = Field(alias="REDIS_DB", default=0)
    cache_time: int = Field(alias="REDIS_CACHE_TIME", default=60)


class FastStreamRabbitMQSettings(BaseSettings):
    host: str = Field(alias="RABBIT_HOST", default="localhost")
    port: int = Field(alias="RABBIT_PORT", default=5672)
    login: str = Field(alias="RABBIT_LOGIN", default="guest")
    password: str = Field(alias="RABBIT_PASSWORD", default="guest")

    @property
    def rabbit_url(self) -> str:
        return f"amqp://{self.login}:{self.password}@{self.host}:{self.port}/"


class Settings(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()
    jwt: JWTSettings = JWTSettings()
    external: ExternalSettings = ExternalSettings()
    redis: RedisSettings = RedisSettings()
    rabbit: FastStreamRabbitMQSettings = FastStreamRabbitMQSettings()

    class Config:
        env_file = "../../../.env"
        env_file_encoding = "utf-8"
        extra = "allow"

from typing import List
from pydantic import BaseSettings, Field


class TgBotSettings(BaseSettings):
    owner_id: int = Field(..., env="TG_OWNER_ID")
    token: str = Field(..., env="TG_BOT_TOKEN")
    throttling_rate: float = Field(..., env="THROTTLING_RATE")
    api_url: str = Field(..., env="TG_API_URL")
    redis_use: bool = Field(..., env="REDIS_USE")

    @property
    def api_is_local(self):
        return self.api_url != "https://api.telegram.org"


class PostgresSettings(BaseSettings):
    user: str = Field(..., env="POSTGRES_USER")
    password: str = Field(..., env="POSTGRES_PASSWORD")
    host: str = Field(..., env="POSTGRES_HOST")
    port: int = Field(..., env="POSTGRES_PORT")
    database: str = Field(..., env="POSTGRES_DB")
    url: str = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        db_url = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"  # noqa
        self.url = db_url.format(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )


class RedisSettings(BaseSettings):
    host: str = Field(..., env="REDIS_HOST")
    port: int = Field(..., env="REDIS_PORT")
    db: int = Field(..., env="REDIS_DB")
    url: str = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "redis://{host}:{port}/{db}".format(
            host=self.host,
            port=self.port,
            db=self.db,
        )


class WebhookSettings(BaseSettings):
    url: str = Field(..., env="WEBHOOK_URL")
    port: int = Field(..., env="WEBHOOK_PORT")
    path: str = Field(..., env="WEBHOOK_PATH")
    drop_pending_updates: bool = Field(..., env="DROP_PENDING_UPDATES")
    use: bool = Field(..., env="WEBHOOK_USE")


class Settings(BaseSettings):
    bot_: TgBotSettings = TgBotSettings()
    postgres: PostgresSettings = PostgresSettings()
    redis_: RedisSettings = RedisSettings()
    webhook: WebhookSettings = WebhookSettings()
    open_api_key: str = Field(..., env="OPEN_API_KEY")
    chat_gpt_model: str = Field(..., env="CHAT_GPT_MODEL")
    main_admin: int = Field(..., env="MAIN_ADMIN")
    admins: List[int] = Field(..., env="ADMINS")
    request_limit: int = Field(..., env="REQUEST_LIMIT")
    context_message_limit: int = Field(..., env="CONTEXT_MESSAGE_LIMIT")

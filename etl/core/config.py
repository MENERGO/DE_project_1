__all__ = ["settings"]

from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_prefix = "ETL_"

    db_name = "news"
    db_user = "news_postgres"
    db_password = "news_password_user"
    db_host = "127.0.0.1"
    db_port = "5433"

    data_folder = "../data"
    state_filepath = 'core/state.json'

    backoff_timeout: int = 3


settings = Settings()

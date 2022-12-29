__all__ = ["consumer"]

import backoff
import psycopg2

from core.config import settings
from core.logger import logger


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(RuntimeError, ConnectionError, TimeoutError),
    max_time=settings.backoff_timeout,
)
def consumer():
    conn = psycopg2.connect(
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_password,
        host=settings.db_host,
        port=int(settings.db_port)
    )
    if conn:
        logger.info(f"consumer - подключился к Postgresql")
    else:
        logger.error(f"consumer - не смог подключиться к Postgresql")
    return conn

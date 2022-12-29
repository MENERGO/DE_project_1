import time

from core.logger import logger
from db.consumer import consumer
from db.producer import producer
from services.services import etl_process

logger.info("ETL - логирование ETL_news началось")
consumer = consumer()
producer = producer()


def main():
    # time.sleep(10)
    etl_process(producer, consumer)


if __name__ == "__main__":
    main()

__all__ = ["logger"]

import logging


def get_logger(name):
    formatter = logging.Formatter(
        fmt=f"%(asctime)s - [%(levelname)s] - %(name)s - "
            f"(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    loger = logging.getLogger(name)
    loger.setLevel(logging.INFO)
    loger.addHandler(handler)
    return loger


logger = get_logger("ETL_news")

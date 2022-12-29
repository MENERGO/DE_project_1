import json
import os
import requests
import urllib3

from datetime import datetime, timedelta
from logger import logger

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    list_sources: dict = {
        'vedomosti': 'https://www.vedomosti.ru/rss/news',
        'lenta': 'https://lenta.ru/rss/',
        'tass': 'https://tass.ru/rss/v2.xml',
    }

    headers: json = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    basedir: str = 'data/'
    t: datetime = datetime.today() + timedelta(hours=3)
    year: str = str(t.year)
    month: str = str(t.month)
    day: str = str(t.day)

    for source in list_sources.keys():
        if not os.path.exists(basedir + source):
            os.makedirs(basedir + source)
        if not os.path.exists(basedir + source + '/' + year):
            os.makedirs(basedir + source + '/' + year)
        if not os.path.exists(basedir + source + '/' + year + '/' + month):
            os.makedirs(basedir + source + '/' + year + '/' + month)

    for source, url in list_sources.items():
        response = requests.get(url, headers=headers, verify=False, timeout=5)
        with open(os.path.join(basedir, source + '.txt'), 'wb') as row_file:
            row_file.write(response.content)
            logger.info(f"parser - сохранен rss из {source} для регулярного чтения")
        with open(os.path.join(basedir + source + '/' + year + '/' + month,
                               year + '_' + month + '_' + day + '_' + source + '.txt'), 'wb') as row_file:
            row_file.write(response.content)
            logger.info(f"parser - сохранен rss из {source} для архива")


if __name__ == "__main__":
    main()

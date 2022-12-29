__all__ = ["producer"]

import datetime as dt
import feedparser
import os

from core.config import settings
from core.logger import logger
from services.state import JsonFileStorage, State
from services.transformer import transformer


def producer():
    def transform_to_list(data, mark):
        previous_time = None
        new_news_time = None
        for n, entry in enumerate(data.entries):
            news_time = dt.datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z').timestamp()
            if n == 0:
                new_news_time = news_time
                previous_time = time_mark[mark][1]
            if previous_time < news_time:
                article_list.append(transformer(entry, mark))
        time_mark[mark][1] = new_news_time

    state = State(JsonFileStorage(settings.state_filepath))
    data_folder: str = settings.data_folder
    article_list = []

    mark_lenta = 'Lenta.ru : Новости'
    mark_vedomosti = '"Ведомости". Ежедневная деловая газета'
    mark_tass = 'ТАСС'

    time_mark = {mark_lenta: state.get_state(mark_lenta),
                 mark_vedomosti: state.get_state(mark_vedomosti),
                 mark_tass: state.get_state(mark_tass)}

    if time_mark == {mark_lenta: None, mark_vedomosti: None, mark_tass: None}:
        path_list_row = [os.path.join(dp, f).replace('\\', '/')
                         for dp, dn, filenames in os.walk(data_folder)
                         for f in filenames if os.path.splitext(f)[1] == '.txt']
        path_list = path_list_row[3:]
        time_mark = {mark_lenta: [1632135515.813837, 1602135515.813837],
                     mark_vedomosti: [1652135515.813837, 1601135515.813837],
                     mark_tass: [1641135515.813837, 1601135515.813837]
                     }
    else:
        path_list = []
        for filename in os.listdir(data_folder):
            if filename.find('.txt') > 0:
                path_list.append(data_folder + '/' + filename)

    for filename in path_list:
        html = feedparser.parse(filename)
        file_updated = os.path.getmtime(filename)

        if html['feed']['title'] == mark_lenta and time_mark[html['feed']['title']][0] < file_updated:
            time_mark[html['feed']['title']][0] = file_updated
            transform_to_list(html, mark_lenta)
        elif html['feed']['title'] == mark_tass and time_mark[html['feed']['title']][0] < file_updated:
            time_mark[html['feed']['title']][0] = file_updated
            transform_to_list(html, mark_tass)
        elif html['feed']['title'] == mark_vedomosti and time_mark[html['feed']['title']][0] < file_updated:
            time_mark[html['feed']['title']][0] = file_updated
            transform_to_list(html, mark_vedomosti)
        else:
            logger.info(f"producer - Новых версий файла {filename} нет.")
    return article_list, time_mark, state

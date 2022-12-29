__all__ = ["etl_process"]

import backoff
import time
import uuid

from core.logger import logger
from datetime import datetime as dt
from psycopg2 import sql


def read_dicts(cur, table) -> dict:
    cur.execute(sql.SQL(f'''select content.{table}.title, content.{table}.id
                            from content.{table};
                        ''')
                )
    table_dict = {k: v for k, v in cur.fetchall()}
    if not table_dict:
        table_dict = {}
    return table_dict


@backoff.on_exception(
    backoff.expo, exception=(RuntimeError, ConnectionError, TimeoutError), max_tries=5
)
def etl_process(producer_data, consumer) -> None:
    producer, time_mark, state = producer_data
    cur = consumer.cursor()

    source_dict: dict = read_dicts(cur, 'source')
    category_dict: dict = read_dicts(cur, 'category')
    author_dict: dict = read_dicts(cur, 'author')

    for n, x in enumerate(producer):
        if x == producer[n - 1]:
            continue
        logger.info(f"Work with {x.title} from {x.source}  ===  {x.pubDate}")
        article_id = uuid.uuid4()
        if x.source not in source_dict.keys():
            source_id = uuid.uuid4()
            source_dict[x.source] = source_id
            cur.execute(
                sql.SQL(f"""INSERT INTO content.source
                       (id,title,is_active,created_at,updated_at)
                       VALUES
                       ('{source_id}', '{x.source}', TRUE, '{dt.now()}', '{dt.now()}')
                       ON CONFLICT (title) DO NOTHING
                        """
                        )
            )
            consumer.commit()

        cur.execute(
            (f"""INSERT INTO content.article
           (id,source_id,title,guid,link,pdalink,enclosure_url,description,pubDate,is_active,created_at,updated_at)
           VALUES
           ('{article_id}','{source_dict[x.source]}','{x.title}', '{x.guid}','{x.link}','{x.pdalink}',
           '{x.enclosure_url}','{x.description}', '{x.pubDate}', TRUE,'{dt.now()}', '{dt.now()}')
            """)
        )
        consumer.commit()

        for category in x.category:
            if category not in category_dict.keys():
                category_id = uuid.uuid4()
                category_dict[category] = category_id
                cur.execute(
                    (f"""INSERT INTO content.category
                           (id,title,is_active,created_at,updated_at)
                           VALUES
                           ('{category_id}', '{category}', TRUE, '{dt.now()}', '{dt.now()}')
                            """
                     )
                )
                consumer.commit()
            category_id = category_dict[category]
            x_id = uuid.uuid4()
            cur.execute(
                f"""INSERT INTO content.category_article
               (id, article_id,category_id,created_at)
               VALUES
               ('{x_id}','{article_id}', '{category_id}', '{dt.now()}')
                """
            )
            consumer.commit()

        for author in x.author:
            if author not in author_dict.keys():
                author_id: uuid = uuid.uuid4()
                author_dict[author]: uuid = author_id
                cur.execute(
                    sql.SQL(f"""INSERT INTO content.author
                            (id,title,is_active,created_at,updated_at)
                            VALUES
                            ('{author_id}', '{author}', TRUE, '{dt.now()}', '{dt.now()}')
                             """
                            )
                )
                consumer.commit()
            author_id = author_dict[author]
            x_id = uuid.uuid4()
            cur.execute(
                f"""INSERT INTO content.author_article
                (id, article_id,author_id,created_at)
                VALUES
                ('{x_id}','{article_id}', '{author_id}', '{dt.now()}')
                 """
            )
            consumer.commit()

        time.sleep(0.1)
        logger.info(f"ETL-процесс - успешно прошла запись в Postgresql")
    consumer.close()

    state.set_state(time_mark)
    logger.info(f'ETL-процесс - сохранили состояние с датой {time_mark}.')

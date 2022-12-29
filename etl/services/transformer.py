__all__ = ["transformer"]

import datetime as dt

from dataclasses import dataclass
from typing import Type


@dataclass(frozen=True)
class Article:
    title: str
    guid: str = None
    link: str = None
    pdalink: str = None
    enclosure_url: str = None
    description: str = None
    pubDate: dt.date = None
    is_active: bool = True
    source: str = None
    author: list[str] = None
    category: list[str] = None


def transformer(row, source) -> Type[Article]:
    description = row.get('description', None)
    if description:
        description = description.replace("'", "`")
    title = row.get('title', None).replace("'", "`")

    enclosure_url = None
    category: list = []
    authors: list = []
    if 'authors' in row and source != '"Ведомости". Ежедневная деловая газета':
        for author in row.authors:
            authors.append(author['name'])
    if 'tags' in row:
        for tag in row.tags:
            category.append(tag['term'])
    else:
        category.append('Нет категории')
    if len(row.links) > 1:
        enclosure_url = row.links[1].href

    article = Article(
        title=title,
        guid=row.get('guid', None),
        link=row.get('link', None),
        pdalink=row.get('pdalink', None),
        enclosure_url=enclosure_url,
        description=description,
        pubDate=row.get('published', None),
        is_active=True,
        source=source,
        author=authors,
        category=category
    )
    return article

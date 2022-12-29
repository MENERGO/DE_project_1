-- CREATE DATABASE news;
-- \c news;
CREATE SCHEMA IF NOT EXISTS content;
-- CREATE EXTENSION "uuid-ossp";

CREATE TABLE IF NOT EXISTS content.source
(
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title      VARCHAR(100) NOT NULL UNIQUE,
    is_active  BOOLEAN          DEFAULT TRUE,
    created_at timestamptz      DEFAULT NOW(),
    updated_at timestamptz      DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS content.article
(
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id     UUID,
    title         VARCHAR(255) NOT NULL,
    guid          TEXT         NOT NULL UNIQUE,
    link          TEXT         NOT NULL UNIQUE,
    pdalink       TEXT,
    enclosure_url TEXT,
    description   TEXT,
    pubDate       TIMESTAMP,
    is_active     BOOLEAN          DEFAULT TRUE,
    created_at    timestamptz      DEFAULT NOW(),
    updated_at    timestamptz      DEFAULT NOW(),
    FOREIGN KEY (source_id) REFERENCES content.source (id)
);

CREATE TABLE IF NOT EXISTS content.author
(
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title      VARCHAR(100) NOT NULL,
    is_active  BOOLEAN          DEFAULT TRUE,
    created_at timestamptz      DEFAULT NOW(),
    updated_at timestamptz      DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS content.author_article
(
    id         UUID PRIMARY KEY,
    article_id UUID NOT NULL,
    author_id  UUID NOT NULL,
    created_at timestamp with time zone
);

CREATE UNIQUE INDEX IF NOT exists article_author ON content.author_article (article_id, author_id);

CREATE TABLE IF NOT EXISTS content.category
(
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title      VARCHAR(255) NOT NULL UNIQUE,
    is_active  BOOLEAN          DEFAULT TRUE,
    created_at timestamptz      DEFAULT NOW(),
    updated_at timestamptz      DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS content.category_article
(
    id          UUID PRIMARY KEY,
    article_id  UUID NOT NULL,
    category_id UUID NOT NULL,
    created_at  timestamp with time zone
);

CREATE UNIQUE INDEX IF NOT exists article_category ON content.category_article (article_id, category_id);

-- CREATE TABLE IF NOT EXISTS content.source_article
-- (
--     id         UUID PRIMARY KEY,
--     article_id UUID NOT NULL,
--     source_id  UUID NOT NULL,
--     created_at timestamp with time zone
-- );
--
-- CREATE UNIQUE INDEX IF NOT exists article_source ON content.source_article (article_id, source_id);

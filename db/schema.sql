CREATE TABLE IF NOT EXISTS raw_posts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    source      TEXT NOT NULL,
    external_id TEXT,
    title       TEXT,
    description TEXT,
    url         TEXT,
    author      TEXT,
    likes       INTEGER DEFAULT 0,
    comments    INTEGER DEFAULT 0,
    views       INTEGER DEFAULT 0,
    shares      INTEGER DEFAULT 0,
    scraped_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source, external_id)
);

CREATE TABLE IF NOT EXISTS patterns (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    analyzed_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_filter      TEXT,
    post_count         INTEGER,
    top_hooks          TEXT,
    content_formats    TEXT,
    keywords           TEXT,
    engagement_signals TEXT,
    avoid              TEXT,
    model_used         TEXT,
    input_tokens       INTEGER,
    output_tokens      INTEGER
);

CREATE TABLE IF NOT EXISTS generated_content (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    pattern_id    INTEGER REFERENCES patterns(id),
    topic         TEXT NOT NULL,
    platform      TEXT NOT NULL,
    hook          TEXT,
    body          TEXT,
    cta           TEXT,
    hashtags      TEXT,
    formatted     TEXT,
    status        TEXT DEFAULT 'draft',
    generated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    posted_at     TIMESTAMP,
    model_used    TEXT,
    input_tokens  INTEGER,
    output_tokens INTEGER
);

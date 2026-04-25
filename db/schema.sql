CREATE TABLE IF NOT EXISTS clips (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path        TEXT NOT NULL,
    title            TEXT,
    notes            TEXT,
    duration_seconds INTEGER,
    recorded_at      TIMESTAMP,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(file_path)
);

CREATE TABLE IF NOT EXISTS captions (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    clip_id       INTEGER NOT NULL REFERENCES clips(id),
    platform      TEXT NOT NULL,
    hook          TEXT,
    body          TEXT,
    hashtags      TEXT,
    model_used    TEXT,
    input_tokens  INTEGER,
    output_tokens INTEGER,
    generated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS schedules (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    clip_id       INTEGER NOT NULL REFERENCES clips(id),
    caption_id    INTEGER NOT NULL REFERENCES captions(id),
    platform      TEXT NOT NULL,
    scheduled_for TIMESTAMP NOT NULL,
    status        TEXT NOT NULL DEFAULT 'queued'
                  CHECK (status IN ('queued', 'posted', 'failed')),
    posted_url    TEXT,
    posted_at     TIMESTAMP,
    UNIQUE(clip_id, platform, scheduled_for)
);

CREATE TABLE IF NOT EXISTS metrics (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    schedule_id INTEGER NOT NULL REFERENCES schedules(id),
    views       INTEGER,
    likes       INTEGER,
    comments    INTEGER,
    shares      INTEGER,
    fetched_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

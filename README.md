# content-engine

AI content distribution + trend analysis engine. Scrapes Reddit and YouTube for trending content in the game-dev / Roblox niche, uses Claude to extract reusable patterns, and generates platform-specific drafts (TikTok scripts, YouTube Shorts, Twitter threads, Instagram captions).

Personal-use CLI. SQLite for storage. No infra.

## Setup

```powershell
git clone https://github.com/MiggyDev619/content-engine.git
cd content-engine
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# fill in keys you need (see below)
```

## Credentials

All keys live in `.env` (gitignored). `.env.example` is the template.

| Key | Required for | How to get |
|---|---|---|
| `REDDIT_USER_AGENT` | Reddit scraping | No OAuth — public JSON. Set to `<app>/<version> by u/<your-reddit-username>`. Reddit blocks default httpx UAs. |
| `YOUTUBE_API_KEY` | YouTube scraping | Google Cloud Console → enable YouTube Data API v3 → create API key. Free quota: 10k units/day. |
| `ANTHROPIC_API_KEY` | Pattern analysis + content generation | console.anthropic.com → API Keys. Not needed until Week 3. |
| `APIFY_API_TOKEN` | TikTok scraping (deferred) | apify.com — managed actor, ~$5/mo. |
| `TWITTER_*` | Auto-posting (deferred) | developer.twitter.com Basic tier. Not needed until Week 5. |

## Usage

```powershell
# Scrape trending posts from a subreddit
python main.py scrape --source reddit --subreddit gamedev --limit 25

# Scrape trending YouTube videos for a query
python main.py scrape --source youtube --query "roblox game dev" --limit 25

# Query the DB — top posts by likes, optionally filtered by source
python main.py query --top 10
python main.py query --top 10 --source reddit
```

Re-running the same `scrape` is idempotent — `INSERT OR IGNORE` on the `UNIQUE(source, external_id)` constraint silently dedups.

## Project state

- **Phase 1 — multi-source scrape:** Reddit ✅ live · YouTube ✅ live · TikTok deferred (Apify)
- **Phase 2 — pattern analysis (Claude):** not started
- **Phase 3 — content generation:** not started
- **Phase 4 — automation + scheduling:** not started

See `ROADMAP.md` for the full 6-week plan and `DEVLOG-NOTES.md` for a session-by-session log of what was built and why.

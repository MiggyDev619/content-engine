# content-engine

Cross-post short-form video content (TikTok, YouTube Shorts, Twitter/X, Instagram Reels), schedule posts, draft captions/hooks via Claude, and aggregate per-platform analytics into one CLI view.

Solo-dev tool. Personal use. CLI-first. SQLite for storage. No infrastructure.

> This project pivoted from a content-scraping pipeline on Day 5 — the old direction was solving the wrong problem (the bottleneck is recording clips, not generating ideas). See `DEVLOG-NOTES.md` for the full story.

## Setup

```powershell
git clone https://github.com/MiggyDev619/content-engine.git
cd content-engine
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# fill in keys you actually need (see "Credentials" — most aren't required for MVP)
```

## Credentials

All keys live in `.env` (gitignored). `.env.example` is the template.

| Key | Required for | How to get |
|---|---|---|
| `ANTHROPIC_API_KEY` | `caption draft` | console.anthropic.com → API Keys |
| `YOUTUBE_API_KEY` | `metrics pull` for YouTube Shorts | Google Cloud Console → enable YouTube Data API v3 |
| `TWITTER_*` | Auto-post + analytics for X | Deferred (Basic tier $100/mo) — leave blank for MVP |

## Usage

```powershell
# Register a recorded clip
python main.py clip add "E:\clips\dms-loadout.mp4" --title "Loadout reveal" --duration 23

# Draft per-platform captions for a clip via Claude  (Phase 1, in progress)
python main.py caption draft 1 --platform all

# Schedule a clip+caption for a specific platform and time
python main.py schedule 1 --caption-id 4 --platform tiktok --datetime "2026-04-28 18:00"

# See what's queued this week
python main.py queue

# Pull analytics — YouTube auto; manual entry for everything else
python main.py metrics pull
python main.py metrics record 7 --views 12000 --likes 340 --at "2026-04-30 09:00"
python main.py metrics show --days 7
```

Why manual entry for TikTok / Instagram / X: TikTok has no public personal-account analytics API; Instagram needs a Business account + Meta Graph; X requires the Basic API tier ($100/mo). Manual snapshot entry is the design, not a workaround.

## Project state

| Phase | Goal | Status |
|---|---|---|
| Phase 1 | Cross-poster MVP — `clip` + `caption` + `schedule` + `queue` | `clip add` shipped; rest in progress |
| Phase 2 | Analytics — `metrics pull` (YouTube auto) + `record` (manual) + `show` | queued |
| Phase 3 | Quality of life — `ffprobe`, Buffer integration if needed | optional |

See `ROADMAP.md` for the phase breakdown and `DEVLOG-NOTES.md` for session-by-session build notes.

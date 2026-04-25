# content-engine

Solo-dev tool for cross-posting short-form video content (TikTok, YouTube Shorts, Twitter/X, Instagram Reels), scheduling posts, drafting captions/hooks via Claude, and aggregating per-platform analytics into one CLI view.

Personal use, single user, CLI-first. SQLite. No infrastructure, no deployment.

Part of a three-project portfolio: clips originate from `discord-mod-simulator` (a Roblox game), get processed and scheduled through this tool, and `miggy-devlog` (a separate Vercel site) narrates the build process. Each project is independent — file-on-disk handoffs, no imports.

> The original tool was a scrape→cluster→generate text-content pipeline. That solved the wrong problem (the bottleneck is recording clips, not generating ideas). Pivoted on Day 5; full story in `DEVLOG-NOTES.md`.

## Stack

- Python 3.13, Click CLI, stdlib `sqlite3`
- Anthropic SDK for caption / hook generation
- `httpx` for YouTube Data API (analytics, not scraping)
- `python-dotenv`

## Running

```powershell
.\venv\Scripts\Activate.ps1
python main.py --help
python main.py clip add "E:\clips\loadout-reveal.mp4" --title "Loadout reveal" --duration 23
```

On Windows the venv activation path is `venv\Scripts\Activate.ps1` (not `venv/bin/activate`).

## Credentials

All keys in `.env` (gitignored). `.env.example` is the template.

| Key | Used for | Required when |
|---|---|---|
| `ANTHROPIC_API_KEY` | Caption / hook generation | Phase 1 (`caption draft` onward) |
| `YOUTUBE_API_KEY` | Shorts analytics auto-pull | Phase 2 (`metrics pull`) |
| `TWITTER_*` | Auto-post + analytics for X | Deferred (Basic tier $100/mo) |

## Schema (mental model)

```
clips → captions → schedules → metrics
```

Four tables. `clips` is the root. Each clip has multiple captions (drafts per platform). A `schedule` row commits a specific clip+caption+platform to a posting time. Each posted schedule accumulates `metrics` snapshots over time.

UNIQUE constraints enforce intent at the schema, not in Python:
- `clips.file_path` — same file can't double-register
- `schedules.(clip_id, platform, scheduled_for)` — can't double-book a slot
- `schedules.status` — `CHECK (status IN ('queued', 'posted', 'failed'))`

`captions` and `metrics` deliberately have no UNIQUE — multiple drafts per platform is the feature; metrics are time-series snapshots.

## Build order (locked, vertical slice per command)

1. ✅ `clip add`
2. `caption draft <clip-id> [--platform]`
3. `schedule <clip-id> --caption-id ... --platform ... --datetime ...`
4. `queue`
5. `metrics pull` (YouTube auto)
6. `metrics record` (manual entry for non-YouTube platforms)
7. `metrics show`

Each slice = schema check + DB function + CLI command + smoke test + commit. Stubs raise `NotImplementedError` so accidental early calls fail loudly.

## Model strategy — hybrid Opus / Sonnet

| Stage | Model | Why |
|---|---|---|
| Hook / caption brainstorming | `claude-opus-4-7` | Quality and novelty matter; <100 captions/week, cost is fine |
| Per-platform mechanical reformat | `claude-sonnet-4-6` | Length / hashtag / aspect-ratio adjustments are mechanical; Sonnet is 5× cheaper |

Every `captions` row records `model_used`, `input_tokens`, `output_tokens` so cost-per-caption is visible in the DB. Cost visibility is a milestone, not a nice-to-have.

## Opus 4.7 API quirks

These WILL cause 400 errors if you ignore them:

- **No `temperature`, `top_p`, or `top_k`.** Tone and style are prompt-only.
- **No prefill / assistant-turn priming.** For structured output, use JSON-mode-style prompts that ask for a JSON object, and parse the response.
- Pin model IDs explicitly. Don't rely on aliases.

## Sharp edges

- **`metrics pull` is YouTube-only-auto. Don't try to fix TikTok / IG / X autopull.** TikTok has no public personal-account analytics API. Instagram needs a Business account + Meta Graph. X requires the $100/mo Basic tier. Manual entry via `metrics record` is the design, not a temporary state. The `metrics pull` docstring spells this out so future-me doesn't waste a session trying to "fix" the missing autopull.
- **`--caption-id` is required on `schedule`.** Implicit "latest" bites at 11pm when three drafts exist and the wrong one ships. Same enforcement-at-the-boundary energy as `INSERT OR IGNORE` over fetch-check-insert.
- **`schedules.status` is CHECK-constrained.** Bypassing with raw SQL UPDATE will fail. That's the point — typo'd `'posted '` (trailing space) won't silently break `queue` filters.
- **Stubs in `db/database.py` raise `NotImplementedError`**, not silent stub returns. Catches typos when a future command tries to call them too early.
- **Don't add thumbnails.** Different scope, image-gen cost, and Shorts/Reels autoplay in feed. Struck from goals.
- **Don't reach for Buffer / Publer until manual upload pain is real.** YAGNI applies.
- **Don't add Redis / Celery / Postgres / Docker / FastAPI.** Single user, CLI, SQLite to 100k+ rows. None of these solve a problem we have.
- **Aspect ratio is a printed checklist at `schedule` time, not a schema column.** The MP4 has the ratio baked in when recorded.

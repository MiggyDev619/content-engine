# content-engine

Python CLI that scrapes trending content (Reddit, YouTube, TikTok), uses Claude to extract patterns, and generates platform-specific drafts (TikTok, YouTube Shorts, Twitter/X, Instagram).

Part of a three-project portfolio: this engine feeds drafts into the devlog site; the Roblox game `discord-mod-simulator` is the subject/topic input.

## Stack

- Python 3.13, Click CLI, SQLite (via `sqlite-utils`)
- Reddit: PRAW · YouTube: Data API v3 via httpx · TikTok: Apify managed actor
- Anthropic SDK for analysis + generation
- APScheduler for daily runs, Tweepy for Twitter auto-post

## Running

```powershell
.\venv\Scripts\Activate.ps1
python main.py --help
python main.py scrape --source reddit --subreddit gamedev
```

On Windows the venv activation path is `venv\Scripts\Activate.ps1` (not `venv/bin/activate`).

## Credentials

All keys in `.env` (never committed). Reddit, YouTube, Anthropic, Apify, Twitter. `.env` is loaded in `main.py` via `python-dotenv`.

## Structure

See `ROADMAP.md` for the full 6-week plan and directory layout. Build order is strict — each layer depends on the previous one:

1. `db/` → 2. `scrapers/` → 3. `analyzer/` → 4. `generator/` + `formatter/` → 5. `pipeline.py` → 6. `poster/`

## Model strategy — hybrid Opus / Sonnet

Cost-conscious default. Daily pipeline runs roughly $8/mo hybrid vs ~$12/mo pure-Opus, dropping to $3–6/mo once caching + batch API are on.

| Stage | Model | Why |
|---|---|---|
| `analyzer/` — pattern extraction | `claude-opus-4-7` | Reasoning-heavy; quality drives every downstream step |
| `generator/` — content drafts | `claude-opus-4-7` | Creative generation, style matching |
| `formatter/` — per-platform reshape | `claude-sonnet-4-6` | Mechanical rewrite, Sonnet is sufficient and 5x cheaper |

Every AI-generated row in `patterns` and `generated_content` must record `model_used`, `input_tokens`, `output_tokens`. Cost visibility is a milestone, not a nice-to-have.

Once the pipeline runs daily, the next two optimizations are:
1. **Prompt caching** on the patterns/system prompt (~40–60% off the analyze step)
2. **Message Batches API** for the nightly batch (50% off across the board)

## Opus 4.7 API quirks

These WILL cause 400 errors if you ignore them:

- **No `temperature`, `top_p`, or `top_k`.** Tone and style are prompt-only. Do not pass these fields to the SDK — the request fails.
- **No prefill / assistant-turn priming.** For structured output, use JSON-mode-style prompts that ask the model to return a JSON object, and parse the response.
- Pin the model ID explicitly in every call. Don't rely on aliases.

## Sharp edges

- Do not build a custom TikTok scraper. Use Apify.
- No auto-posting to TikTok or Instagram personal accounts — API doesn't exist. Twitter/X only for MVP.
- Any reference in `ROADMAP.md` to `claude-sonnet-4-20250514` is stale — use the model strategy table above.
- Don't add Redis/Celery/Postgres/Docker until the CLI is running daily. SQLite is fine to 100k+ rows for this use case.

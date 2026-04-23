# content-engine — devlog notes

Raw build notes for the content-engine project, structured for a devlog-generation session to consume.

## How to use this file

- Each dated section is one work session's deliverables, decisions, and hooks.
- The devlog session should pick one or two **narrative angles** from the "Hooks for the post" list per section — not try to cover everything.
- Voice: match existing posts in the devlog repo. This file is raw material, not a draft.
- Newest entries at the top.

---

## 2026-04-23 — Day 1: project scaffold

### What got built

- New repo at `E:\Web Development\content-engine\`, git initialized
- Python 3.13 virtualenv, packages installed: `praw`, `anthropic`, `click`, `sqlite-utils`, `httpx`, `python-dotenv`, `apscheduler`, `tweepy`
- `main.py` — Click CLI with four stub commands: `scrape`, `analyze`, `generate`, `query`
- `db/schema.sql` — three tables: `raw_posts`, `patterns`, `generated_content`
- Token tracking columns added on `patterns` and `generated_content` (`model_used`, `input_tokens`, `output_tokens`) — cost visibility from day one
- Project docs: `ROADMAP.md` (6-week plan), `CLAUDE.md` (session context for future Claude Code sessions)
- `.env` (gitignored) + `.env.example` (checked in template)

Three commits on `master`:
- `765f9f4` — Initial Day 1 scaffold
- `ec3d09b` — schema: add token tracking columns
- `9cc655e` — Add .env.example template

### Decisions made (and why)

**Three projects stay separate, not a monorepo.**
- Roblox game (`discord-mod-simulator`), Vercel devlog (`miggy-devlog`), content-engine — three different stacks (Luau, Next.js, Python), three different cadences.
- Integration is file-based, not import-based. Engine writes markdown drafts into a folder the devlog watches. Game → devlog is frontmatter references + manual screenshots. Game → engine is a string topic, nothing more.
- Acid test: delete any one project's folder, the other two still run.

**Hybrid Claude model strategy: Opus 4.7 for reasoning, Sonnet 4.6 for mechanical work.**
- Pattern analysis + content generation = Opus 4.7 (reasoning-heavy, quality drives everything downstream)
- Per-platform formatting = Sonnet 4.6 (mechanical rewrite, Sonnet is 5x cheaper and sufficient)
- Cost math: pure Opus ~$12/mo for a daily pipeline; hybrid ~$8/mo; with prompt caching + Batch API later, $3–6/mo.
- The optimization ladder matters: once the pipeline runs daily, prompt caching cuts the analyze step 40–60%, and the Message Batches API is another 50% off across the board.

**Opus 4.7 has API quirks that would have bitten us later:**
- No `temperature`, `top_p`, `top_k` — returns 400 errors. Tone is prompt-only.
- No prefill / assistant-turn priming. Structured output via JSON-mode-style prompts.
- Flagged in `CLAUDE.md` so future sessions don't copy stale patterns.

**Token tracking baked into the schema before any rows exist.**
- Three columns on `patterns` and `generated_content`: `model_used`, `input_tokens`, `output_tokens`.
- Cheap to add on empty tables; painful to backfill.
- Cost-per-run is a milestone on the roadmap, not a nice-to-have.

**Deliberate exclusions.**
- No custom TikTok scraper. Use Apify (~$5/mo) — TikTok anti-bot measures break custom scrapers constantly.
- No auto-posting to TikTok or Instagram personal accounts. No API exists. Twitter/X only for MVP.
- No Redis, Celery, Postgres, Docker, FastAPI, ORM, web dashboard. SQLite to 100k rows is fine. One user (me) means CLI beats UI.
- No `temperature=` anywhere in future code.
- No `claude-sonnet-4-20250514` model ID — stale, ignored.

### Cost reality (for posterity)

Rough monthly estimates for the full MVP:
- Anthropic API (hybrid, daily runs): $8/mo → $3–6/mo with caching + batch
- Apify (TikTok scraping, optional): $5/mo
- Twitter/X Basic tier (only needed when auto-post turns on): $100/mo
- YouTube Data API, Reddit API, Vercel Hobby, SQLite: $0

MVP phase realistic total: **$0–$13/mo** (skip Apify, no auto-post yet).

### What's intentionally not built yet

- Actual Reddit scraper (Day 2)
- YouTube scraper (Days 4–5)
- Any AI code at all (Week 3)
- Anything in `scrapers/`, `analyzer/`, `generator/`, `formatter/`, `poster/` folders — these don't exist yet on disk, appear only in the roadmap

### Blockers for Day 2

- Need Reddit API creds (reddit.com/prefs/apps, "script" app type, 5 min)

### Hooks for the post

Pick one. Not all.

- **"Three projects, one brain: how I'm running parallel Claude Code sessions without losing my mind"** — the integration-points rule, file-on-disk handoffs, why I killed the monorepo impulse early.
- **"The hidden cost of 'just use AI for everything'"** — cost math on Opus vs Sonnet, why I went hybrid, what a realistic monthly bill actually looks like for a solo builder.
- **"Day 1 of a 6-week content pipeline"** — scaffold recap, what got locked in as non-negotiable (stack, folder order), what got explicitly banned (custom TikTok scraper, ORM, Docker).
- **"Token tracking is a schema concern, not an observability concern"** — why I added `model_used`/`input_tokens`/`output_tokens` to the DB on day one, before any rows existed.
- **"Opus 4.7 silently dropped three API parameters — here's what breaks"** — the `temperature`/`top_p`/`top_k` removal, why it matters for how prompts are designed.

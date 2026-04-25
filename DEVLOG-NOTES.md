# content-engine — devlog notes

Raw build notes for the content-engine project, structured for a devlog-generation session to consume.

## How to use this file

- Each dated section is one work session's deliverables, decisions, and hooks.
- The devlog session should pick one or two **narrative angles** from the "Hooks for the post" list per section — not try to cover everything.
- Voice: match existing posts in the devlog repo. This file is raw material, not a draft.
- Newest entries at the top.

---

## 2026-04-25 — Day 4: YouTube scraper, query command, README, master→main

### What got built

- **`scrapers/youtube.py`** — `fetch_trending_videos(query, max_results)` using YouTube Data API v3. Two-call: `search.list` to find videos by query, `videos.list` (batched by id) to pull engagement stats. Returns dicts shaped to match `raw_posts`. Quota cost per scrape: 101 units against 10k daily.
- **`main.py` updates** — `scrape` command got a `--query` flag and a wired YouTube branch alongside Reddit. `query` command rewired to call `db.database.get_posts` and print formatted `[score] title` + url lines.
- **`README.md`** — public-facing setup + credentials table + usage examples + project-state checklist. Distinct from `CLAUDE.md` (internal context).
- **`master` → `main` migration** — local rename, remote `main` pushed and default flipped on GitHub, remote `master` deleted. Repo is now `https://github.com/MiggyDev619/content-engine` (public) on `main`.
- **Verified end-to-end** — `query --top 5 --source reddit` returned five real rows from yesterday's r/gamedev scrape. `scrape --source youtube` without `--query` errors cleanly. `scrape --source all` without flags skips both real sources gracefully. YouTube live-fetch deferred until `YOUTUBE_API_KEY` is set.

### Decisions made (and why)

- **Two-call YouTube fetch (`search.list` + `videos.list`).** `search.list` returns titles, descriptions, channel — but no view/like/comment counts. Trend analysis needs engagement signal, so a second batched call to `videos.list` is required. 100 + 1 = 101 quota units per scrape against a 10k daily quota — comfortable headroom. Rejected: dropping engagement stats (kills the trend signal we're optimizing for), scraping the YouTube web front page (fragile, against ToS).

- **Click param renamed `query` → `query_` internally.** The `query` CLI subcommand and the `--query` option both exist in the same module. Click would have bound the `query` kwarg to the function while the module-level `query` symbol still pointed at the subcommand — workable, but fragile and confusing. Trailing underscore on the parameter avoids the name shadow without changing the user-facing flag.

- **No retry/backoff yet on YouTube 403 / quota.** Personal-scale (one search per scrape, ≤50 results) sits at <1% of the daily 10k quota. Adding backoff before hitting a real failure is speculation. Same call as the 429 decision on Reddit.

- **README and `CLAUDE.md` stay separate.** Same project, different audiences. README is for someone landing on the GitHub repo from a blog post or a search result — needs setup commands, credentials table, what-it-does. `CLAUDE.md` is for a Claude Code session opening the project — needs decisions, sharp edges, model strategy. Cross-referencing them would couple the two and force every README change into a Claude-context update.

- **Renamed `master` → `main` now, not later.** Repo is ~24h old with one external dependency (zero, actually — no one's linked to it yet). The cost of renaming after a blog post, a tweet, or a portfolio link goes out is meaningfully higher. Four-command migration: `git branch -m`, `git push -u`, `gh repo edit --default-branch`, `git push --delete`. GitHub keeps redirects on the old refs indefinitely.

### What's intentionally not built yet

- TikTok / Apify scraper — Phase 1 close-out, Day 5–7.
- YouTube `pageToken` pagination — current call caps at 50 results per scrape. Add when 50 isn't enough.
- Quota / rate-limit handling — see decision above.
- The analyzer (Phase 2, Week 3).

### Blockers for next session

- **YouTube live verification needs `YOUTUBE_API_KEY`.** Google Cloud Console → create project → enable YouTube Data API v3 → Credentials → Create Credentials → API key → paste into `.env`. ~5 min.
- Optional: Apify account if user wants to start TikTok scraping.

### Hooks for the post

Pick one. Not all.

- **"YouTube's API needs two calls to tell you what trended"** — `search.list` + `videos.list`, why the API design forces this split, and the 100+1 quota cost. Specific technical lesson, useful to anyone building media analytics.
- **"Why my Click parameter is named `query_`"** — two-paragraph mini-post on a name collision between a CLI subcommand and one of its options. Concrete, fixable, easy to understand.
- **"Renaming `master` → `main` on a four-day-old repo"** — quick-win post. Four commands, why now is cheaper than later, the gh-not-on-PATH gotcha.
- **"README is for humans; `CLAUDE.md` is for Claude"** — meta post on splitting public-facing docs from AI-context docs in a project that's actively used by Claude Code. Niche but interesting to anyone running AI-assisted dev workflows.

---

## 2026-04-24 — Day 3: Reddit pivot — PRAW out, public JSON in

### What got built

- **`scrapers/reddit.py` rewritten** — PRAW + OAuth replaced with `httpx.get` against `https://www.reddit.com/r/<subreddit>/top.json`. Function signature, return shape, and caller untouched.
- **Removed `praw` / `prawcore` / `update_checker`** from venv; re-pinned `requirements.txt`. Net change: one fewer dependency cluster.
- **`.env` and `.env.example` cleaned** — dropped `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET`. `REDDIT_USER_AGENT` now flagged in comments as load-bearing.
- **`REDDIT_USER_AGENT` set** to `content-engine/0.1 by u/miggydev`.
- **Live-verified end-to-end** — `python main.py scrape --source reddit --subreddit gamedev --limit 25` landed 25 rows in `content.db`. Re-run inserted 0 new rows — dedup confirmed against the `UNIQUE(source, external_id)` constraint with real Reddit data, not just import tests.
- **Cross-platform handle inventory** — verified `miggydev` is available on YouTube, TikTok, Apify; taken on Reddit (the user's own); status on GitHub, X, Instagram pending or indeterminate. Saved to user-handle memory so future sessions don't re-check.

### Decisions made (and why)

- **Bypassed Reddit's auth flow entirely.** Reddit's Responsible Builder Policy gates self-serve script app creation behind a developer profile + scope review. For a personal-scale project (≤100 reqs/day across a few subs), going through that pipeline is days-to-weeks for uncertain approval. Public JSON endpoints serve our exact need — read-only public subreddit data — and require no OAuth dance. Rejected: applying for Responsible Builder approval (slow, may be denied), pivoting to YouTube-first (loses Reddit's niche signal entirely).

- **User-Agent is load-bearing now, not cosmetic.** Reddit blocks default `python-httpx/X.Y.Z` UAs within seconds. The new `REDDIT_USER_AGENT` value (`content-engine/0.1 by u/miggydev`) is the actual auth substitute. Documented in `.env.example` comments so a future setup doesn't strip it as boilerplate.

- **Function signature stayed identical.** `fetch_top_posts(subreddit, limit, time_filter) -> list[dict]` — same name, same args, same return shape. Caller in `main.py` and storage in `db/database.py` didn't change. Single-file pivot, zero blast radius. Rejected: introducing a `RedditClient` abstraction "to make swapping easier next time" — premature, and the swap was already easy.

- **Removed PRAW outright; no fallback path.** Two implementations of the same function diverge subtly over time and double the maintenance. If the public JSON path breaks, we'll know within a day and pivot then.

- **Standardized on `miggydev` across platforms.** Single canonical handle simplifies attribution, User-Agent strings, blog frontmatter `author`, and audience search. Variant fallbacks (`miggy-dev`, `miggydevhq`) reserved for platforms where `miggydev` is taken.

### What's intentionally not built yet

- 429 backoff / retry. 60 req/min unauth is plenty for daily personal scale. Add the day we actually hit a 429.
- Pushshift / historical Reddit archive integration. Out of scope; never was on the roadmap.
- YouTube scraper (Days 4–5).
- TikTok / Apify (Days 5–7).
- `query` command wire-up and README (Day 4).

### Blockers for next session

- None in code. The Phase 1 multi-source goal is one of three sources done.
- Optional human-side: confirm whether `github.com/MiggyDev` (id 66369572) is the user's old account or a stranger's. Claim `miggydev` on YouTube / TikTok / Apify before squatters appear.

### Hooks for the post

Pick one. Not all.

- **"Reddit closed the API door so I went through the window"** — the policy change, the workaround, the User-Agent gotcha, why public JSON is the right answer for personal-scale. By far the strongest hook: fresh news, real workaround, clear technical lesson, hits an audience hitting the same wall right now.
- **"User-Agent is a load-bearing string"** — short technical post on a header most devs treat as cosmetic. Two paragraphs, one snippet.
- **"Why I deleted PRAW after a 24-hour relationship"** — opinionated mini-post on dropping a dependency rather than maintaining two code paths "just in case."
- **"Checking handle availability across six platforms with curl"** — meta post on what works (GitHub API, YouTube, Apify) and what doesn't (TikTok / X / Instagram SPA gating). Useful for anyone consolidating their online identity.

---

## 2026-04-23 — Day 2: Reddit scraper + DB layer

### What got built

- **`db/database.py`** — `init_db()`, `insert_post()`, `get_posts()`. Raw `sqlite3`, ~50 lines total. `sqlite3.Row` factory so results come back dict-shaped. `INSERT OR IGNORE` against the `UNIQUE(source, external_id)` constraint for silent dedup.
- **`scrapers/reddit.py`** — `fetch_top_posts(subreddit, limit=25, time_filter="day")` returning `list[dict]` pre-shaped to the `raw_posts` schema. PRAW read-only, creds from env.
- **`scrape` command wired in `main.py`** — calls `init_db()` first, then dispatches per `--source`. Late-binds imports inside the command body so the per-source client only loads when needed. Prints `scraped N, M new rows` so dedup behavior is visible.
- **DB auto-initializes on first scrape** — `content.db` (24 KB) appears at repo root, all three tables present, schema matches validation from Day 1.
- **Verified** — `python main.py scrape --source all --limit 5` runs cleanly without Reddit creds (gracefully skips reddit, echoes stubs for youtube/tiktok, initializes the DB).

### Decisions made (and why)

- **Raw `sqlite3`, not `sqlite-utils`.** `sqlite-utils` is installed and fine, but the whole DB module fits in ~50 lines of stdlib `sqlite3`. One less abstraction to learn, queries read like SQL. Rejected: reaching for the convenience library when the need hasn't arrived.

- **`INSERT OR IGNORE` for dedup.** `UNIQUE(source, external_id)` in the schema plus `INSERT OR IGNORE` gives silent dedup in one round-trip. Rejected: SELECT-then-INSERT (race condition, two queries), an ORM's `get_or_create` (adds a dependency for something SQL already does).

- **Late-binding scraper imports inside the command.** `from scrapers.reddit import fetch_top_posts` lives inside the `scrape` command body, not at module top. So `python main.py --help` and other subcommands don't pay the PRAW import cost, and a broken scraper doesn't take down the whole CLI. Rejected: top-of-module imports (cleaner-looking, but couples unrelated subcommands).

- **`time_filter="day"` as the Reddit default.** Trend analysis cares about recent + popular, not all-time. "day" surfaces what's moving now; "all" surfaces the subreddit's greatest hits. Day wins for this pipeline; can be overridden per call.

- **`--source reddit` without `--subreddit` is an error; `--source all` without `--subreddit` is a skip.** Explicit intent to scrape Reddit with no target is user error (fail loud). "Scrape everything" is best-effort (skip what's unconfigured, echo what happened). Same missing input, two meanings, and the CLI says which branch fired.

### What's intentionally not built yet

- YouTube scraper (scheduled for Days 4–5).
- TikTok / Apify integration (Days 5–7).
- `query` command wire-up — currently a stub (Day 3).
- README — deferred to Day 3.
- End-to-end verification run with real Reddit data — blocked on creds.

### Blockers for next session

- **Reddit API credentials.** reddit.com/prefs/apps → "create app" → script type → redirect URI `http://localhost`. Paste `client ID` and `secret` into `.env`. Day 3 opens with `python main.py scrape --source reddit --subreddit gamedev --limit 25` and confirming rows land.

### Hooks for the post

Pick one. Not all.

- **"`INSERT OR IGNORE` is a dedup strategy"** — how a schema constraint plus one SQL keyword replaces a fetch-check-insert loop. Short, specific, useful to anyone writing a scraper.
- **"Writing the scraper before I have the API keys"** — code I can't live-test yet, and why that's the right order. Confidence in the shape comes from type hints and import tests, not live data.
- **"Late-binding imports in a Click CLI"** — why `from scrapers.reddit import …` lives inside the command function, not at module top. Keeps `--help` cheap and lets subcommands fail independently.
- **"Two meanings for the same missing flag"** — `--source reddit` without `--subreddit` errors; `--source all` without `--subreddit` skips. When intent changes the error-handling contract.
- **"SQLite is the default until it isn't"** — why a 50-line stdlib DB layer is the right answer for a solo content pipeline, and what would make me reach for Postgres (spoiler: not yet).

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

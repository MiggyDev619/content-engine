# AI Content Distribution + Trend Analysis Engine
### Execution-Ready Engineering Plan

---

## Honest Framing Before You Start

A few unrealistic ideas to kill now:

- **TikTok scraping is not reliably feasible.** Their anti-bot measures are aggressive and break constantly. Use Apify's managed TikTok scrapers (paid, ~$5/mo) or accept that TikTok is read-only via third-party tools. Do not build a custom TikTok scraper — it will eat weeks.
- **Auto-posting to TikTok is not possible.** No official API for personal accounts. YouTube and Twitter/X have APIs. Instagram requires a Business account + Meta API (annoying but doable). Design for this early.
- **"AI-generated content" alone is not distribution.** This engine gets you raw material. You still have to post and iterate on what performs. Don't confuse automation with growth.
- **This is a 6–8 week project to do well**, not 2 weeks. The plan below is honest about that.

---

## 1. Phased Roadmap

### Phase 1 — Scrape + Store (Weeks 1–2)
**Goal:** Pipeline that pulls trending content and stores it in a queryable format.

Build:
- Reddit scraper via PRAW (official API, free, reliable)
- YouTube scraper via YouTube Data API v3 (free quota: 10k units/day)
- TikTok via Apify actor (managed, no maintenance)
- SQLite database with raw posts table
- CLI command: `python main.py scrape --source reddit --subreddit gamedev`

Done when:
- Running `scrape` command fills database with 50+ posts from 2+ sources
- Data includes title, body/description, engagement metrics, timestamps
- No manual steps required after initial auth setup

---

### Phase 2 — Analyze + Extract Patterns (Week 3)
**Goal:** Claude analyzes scraped content and extracts reusable patterns.

Build:
- Batch analyzer that sends scraped posts to Claude API
- Pattern extraction: hooks, formats, keywords, engagement signals
- Patterns table in DB (linked to source posts)
- CLI command: `python main.py analyze --limit 50`

Done when:
- Running `analyze` on 50 posts returns structured pattern data
- Output includes: top hooks used, content formats, high-engagement keywords
- Results are stored and queryable

---

### Phase 3 — Generate + Format (Week 4)
**Goal:** Claude generates platform-specific content drafts from extracted patterns.

Build:
- Content generator that uses patterns as input
- Platform formatters: TikTok script, YouTube Shorts script, Twitter/X thread, Instagram caption
- Generated content table in DB
- CLI command: `python main.py generate --topic "Roblox game dev" --platform all`

Done when:
- Single command produces 4 platform-ready drafts
- Output is saved to DB and exported as text files
- Quality is good enough to post with minor edits

---

### Phase 4 — Automate + Schedule (Weeks 5–6)
**Goal:** End-to-end pipeline that runs on a schedule and optionally posts.

Build:
- Cron-triggered pipeline: scrape → analyze → generate → export
- Twitter/X auto-post via API
- YouTube Shorts metadata generator (title, description, tags)
- Simple digest: daily email or Slack message with generated drafts
- CLI command: `python main.py run --schedule daily`

Done when:
- Pipeline runs unattended and produces daily content drafts
- At least one platform (Twitter/X) can auto-post
- You're reviewing output, not building

---

## 2. Weekly Execution Plan

### Week 1 — Project Setup + Reddit Scraper
- Day 1–2: Project scaffold, virtualenv, SQLite schema, PRAW setup
- Day 3–4: Reddit scraper working, raw posts saving to DB
- Day 5–7: YouTube Data API v3 scraper, Apify TikTok actor integration

**Output:** `scrape` CLI command pulling from 3 sources

---

### Week 2 — Data Cleaning + Storage Layer
- Day 1–2: Normalize scraped data into consistent schema across sources
- Day 3–4: Deduplication, filtering (remove low-engagement posts)
- Day 5–7: CLI query tool (`python main.py query --top 20 --source reddit`)

**Output:** Clean, queryable dataset of trending content

---

### Week 3 — Claude Analyzer
- Day 1–2: Claude API integration, batch prompt design
- Day 3–4: Pattern extraction working, patterns table populated
- Day 5–7: Keyword frequency analysis, hook library built from real data

**Output:** `analyze` command producing structured pattern data

---

### Week 4 — Content Generator + Platform Formatters
- Day 1–2: Generator prompt design, base content generation working
- Day 3–4: Per-platform formatters (TikTok, YouTube, Twitter, Instagram)
- Day 5–7: File export, review workflow, quality testing on real posts

**Output:** `generate` command producing 4 platform drafts per topic

---

### Week 5 — Pipeline + Scheduling
- Day 1–2: Chain scrape → analyze → generate into single pipeline command
- Day 3–4: APScheduler for daily runs, logging
- Day 5–7: Twitter/X API auto-post, daily digest via email (SMTP)

**Output:** Unattended daily pipeline

---

### Week 6 — Tuning + Personal Use Optimization
- Day 1–2: Fine-tune prompts based on actual generated content quality
- Day 3–4: Add game dev / Roblox-specific context to generators
- Day 5–7: Refactor anything messy, write a basic README

**Output:** System you'd actually use daily

---

## 3. Directory Structure

```
content-engine/
├── main.py                  ← CLI entry point (Click)
├── .env                     ← API keys (never commit)
├── requirements.txt
├── content.db               ← SQLite database
│
├── scrapers/
│   ├── reddit.py            ← PRAW wrapper
│   ├── youtube.py           ← YouTube Data API v3
│   └── tiktok.py            ← Apify REST client
│
├── analyzer/
│   ├── batch.py             ← sends posts to Claude in batches
│   └── patterns.py          ← pattern extraction + storage
│
├── generator/
│   ├── generate.py          ← calls Claude with patterns as context
│   └── prompts.py           ← all prompt templates live here
│
├── formatter/
│   ├── tiktok.py
│   ├── youtube.py
│   ├── twitter.py
│   └── instagram.py
│
├── poster/
│   ├── twitter.py           ← Tweepy wrapper (auto-post)
│   └── queue.py             ← post queue for manual review
│
├── db/
│   ├── schema.sql
│   └── database.py          ← query helpers
│
└── pipeline.py              ← chains scrape → analyze → generate
```

---

## 4. Milestones

| Milestone | Target | Signal |
|---|---|---|
| First data in DB | End of Day 3 | `SELECT COUNT(*) FROM raw_posts` returns 50+ |
| Multi-source scrape | End of Week 1 | Reddit + YouTube both filling DB |
| First pattern extracted | End of Week 3, Day 2 | `patterns` table has one row with real JSON |
| First generated post | End of Week 4, Day 2 | Claude returns a TikTok script worth posting |
| Full platform output | End of Week 4 | One topic → 4 platform drafts in under 60s |
| First automated pipeline | End of Week 5, Day 2 | `python main.py run` completes end-to-end |
| First auto-posted tweet | End of Week 5 | Tweet appears without manual posting |
| Daily unattended run | End of Week 6 | Cron runs at 8am, you review over coffee |

---

## 5. What NOT to Build Yet

- Web dashboard / frontend — CLI is faster
- Multi-user support — not a SaaS yet
- Custom TikTok scraper — use Apify
- TikTok auto-posting — no public API
- Vector embeddings / semantic search — overkill
- ML engagement prediction — not enough labeled data
- Postgres migration — SQLite handles this
- Content approval UI — review exported files manually

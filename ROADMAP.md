# content-engine — roadmap

A solo-dev tool for cross-posting short-form video content (TikTok, YouTube Shorts, Twitter/X, Instagram Reels), scheduling posts, drafting captions/hooks via Claude, and aggregating per-platform analytics into one CLI view.

Personal use, single user, CLI-first. SQLite for storage. No infrastructure, no deployment.

> The original 6-week plan was a scrape→cluster→generate text-content pipeline. That solved the wrong problem — faceless creator accounts grow from gameplay clips, not AI-generated text drafts. The pivot landed on Day 5; full story in `DEVLOG-NOTES.md`.

## Phases

Weekly vertical slices, no fixed deadline. Each phase is "done when it's shippable."

### Phase 1 — clip + caption + schedule MVP

**Done when:** I can register a clip, draft per-platform captions for it, schedule it across platforms, and the `queue` command shows what's coming up.

- [x] `clip add <path>` — register a recorded clip in the DB *(shipped)*
- [ ] `caption draft <clip-id> [--platform]` — Claude generates per-platform captions/hooks
- [ ] `schedule <clip-id> --caption-id ... --platform ... --datetime ...` — record posting intent + print platform-specific upload checklist
- [ ] `queue` — show this week's scheduled posts per platform

### Phase 2 — analytics

**Done when:** `metrics show` gives me a one-screen view of what's working, without opening four apps.

- [ ] `metrics pull` — auto-fetch YouTube Shorts via YouTube Data API + OAuth
- [ ] `metrics record <schedule-id> --views ... --at ...` — manual snapshot entry for TikTok / Instagram / X (no public APIs); `--at` defaults to now() so Sunday batch backfill is friction-free
- [ ] `metrics show [--days N]` — single CLI table: clip | platform | views | likes | comments

### Phase 3 — quality of life (only if specific friction shows up)

- `ffprobe` auto-detect for `--duration` (manual flag is fine for now)
- Buffer / Publer / cross-posting service integration (only if manual upload becomes a real bottleneck)
- YouTube Shorts auto-post via OAuth (when YouTube allows it for non-partner accounts)
- Apify TikTok analytics (only if growth depends on TikTok signal and $5–30/mo is acceptable)

## What NOT to build

- **Thumbnails / image generation.** Shorts and Reels autoplay from feed; custom thumbnails rarely move the needle. Image-gen is different scope, different model, nontrivial cost. Struck from the goals list, not deferred.
- **TikTok auto-post.** No public API for personal accounts.
- **TikTok / Instagram / X analytics auto-pull.** Personal-account analytics aren't available without Business accounts (Meta) or paid tiers (X). `metrics record` is the design, not a workaround. Future-me: don't waste a session trying to "fix" this.
- **Web dashboard / multi-user / Postgres / Docker / Redis.** Single user, CLI is faster, SQLite scales to 100k+ rows for this use case.
- **ML engagement prediction.** No labeled data, and the bottleneck is recording, not ranking.
- **Custom video editing.** Out of scope. The user records elsewhere; this tool starts at "I have a finished MP4."
- **The old scrape → cluster → generate pipeline.** Pivoted away from this on Day 5. See `DEVLOG-NOTES.md`.

## Stack

- Python 3.13, Click CLI, stdlib `sqlite3`
- Anthropic SDK (`claude-opus-4-7` for hooks, `claude-sonnet-4-6` for per-platform reformat)
- `httpx` for YouTube Data API analytics
- `python-dotenv` for `.env`-loaded credentials

## Status

| Phase | Slice | Status |
|---|---|---|
| Phase 1 | `clip add` | ✅ shipped (commits `065564c` → `4eb8693`) |
| Phase 1 | `caption draft` | next |
| Phase 1 | `schedule` + `queue` | queued |
| Phase 2 | `metrics pull` / `record` / `show` | queued |
| Phase 3 | Quality of life | optional |

# content-engine — devlog notes

Raw build notes for the content-engine project, structured for a devlog-generation session to consume.

## How to use this file

- Each dated section is one work session's deliverables, decisions, and hooks.
- The devlog session should pick one or two **narrative angles** from the "Hooks for the post" list per section — not try to cover everything.
- Voice: match existing posts in the devlog repo. This file is raw material, not a draft.
- Newest entries at the top.

---

## 2026-04-25 — Content planning: 10 DMS clips + audit

> Non-numbered entry. Content-strategy session, not a code day. Follow-up to Day 5's pivot — `caption draft` is still stubbed, but you can't build the captioner without first knowing what you're captioning. This session generates the input.

### What got built

- **`docs/clips.md`** — working planning document for the first 10 short-form video clips under the MiggyDev faceless gamedev brand. Per-clip specs (audience, hook copy, body, caption shape, why-it-works, recording requirements), the full posting schedule (Mon / Wed / Fri × ~3.3 weeks), the Sunday batch capture session plan, and a cut-to-6 list for if reality eats four slots. Sourced from the per-entry "Hooks for the post" lists in the sibling DMS repo's `DEVLOG-NOTES.md`.
- **Audience split:** 5 player-facing / 5 dev-facing. Ordered by hook strength (loadout reveal lands first; Phase 1 recap lands tenth) — strongest scroll-stopper at the top because "more from this account" surfaces clip 01 to anyone who finds 02–10 first.
- **Mix targets met:** three broken-or-fixed framings (camera shake, whiff bug, icon iteration), one honestly-imperfect anchor (the still-open whiff question, slot 5), one Phase 1 recap (slot 10), two code-on-screen-as-primary slots (camera shake, empty packet) — at the cap, not over it.
- **Cross-repo correction:** initially wrote `clips.md` and the planning entry into the DMS repo (proximity-of-reading bias — I was reading DMS source for the audit). Moved both to `content-engine` after recognizing the architectural mistake: clips work is content-engine's domain (it's the input for `clip add` / `caption draft` / `schedule`), not DMS's. DMS's `docs/` stays focused on game work; content-engine's `docs/` holds content-pipeline planning. File-on-disk handoff between repos preserved.

### Audit findings (post-plan, same session)

After locking the plan, audited each clip against the actual DMS source. Material findings — full per-clip detail in `docs/clips.md` Audit section:

- **Clip 02 caption is backwards.** Spec said "kick gets eaten by the slow." Actual status priority is **Kick > Timeout > Mute > seek** (`EnemySpawner.server.lua:181-195` in DMS, CLAUDE.md confirms). Kick OVERRIDES Mute, not the inverse. Caption rewrite required before posting.
- **Clip 02 coin payoff doesn't fire on Kick.** Coins only awarded in `banEnemy.OnServerEvent` (`EnemySpawner.server.lua:315`); Kick is non-destructive. If the chain ends on Kick, "+20 coins" floater never appears. Decision needed: end on Kick (no payoff) or on Ban (real popup).
- **Clip 03 has no "before" version in repo.** `git log --follow` on DMS's `BanHammerScript.client.lua` shows it already used `Humanoid.CameraOffset` from the initial Days 1-7 commit. The CFrame-tween version was never committed — has to be **written from scratch** on a throwaway branch, not restored.
- **Clip 08 premise is structurally false.** DMS code sends `kickEnemies:FireServer(lookDir)` (Vector3 payload, not empty) and server reads the client's vector (not its own). Commit `a419aca` documents the switch from server-derived to client-derived as the intentional exception to server-authoritative. The whole "empty packet, server-derived geometry" hook is the inverse of reality. Recommend deferring to week 4+ for a deliberate reconception.
- **Clips 04 & 07 oversell their visuals.** Both spec a "screen flash"; actual behavior is just a label color change in the existing HealthLabel/WaveLabel slots. No full-screen overlay exists in DMS. Decision: accept smaller visuals or add a 20-min `FlashOverlay` Frame in DMS that does double duty.
- **Clip 10 caption claim ("~350 lines of Luau") needs verification** post Days 9-11. Tally with `wc -l src/**/*.lua` in DMS, or drop the clip entirely (recommended — push to week 4+ as a Phase 2 companion).
- **Tool TextureIds are Studio-only state** in DMS, not in the repo. Confirm Sunday morning before recording — fresh place file would have blank icons.

Hard blockers before camera rolls: reconceive Clip 08, rewrite Clip 02 caption, build a temp solo-spawn debug for Clip 02 isolation in DMS, verify Tool TextureIds in DMS Studio. Six items of polish below those, in priority order, in `docs/clips.md`.

### Decisions made (and why)

- **Clip planning lives in `content-engine`, not in `discord-mod-simulator`.** The clips ARE gameplay from DMS, but the *plan* is content-pipeline input — the same data shape the eventual `caption draft`, `schedule`, and `metrics` commands will operate on. Putting `clips.md` in DMS would couple the two repos via a working planning doc that gets edited weekly. Keeping it in content-engine respects the integration-points rule (file-on-disk handoffs between repos, no cross-project writes for unrelated work). DMS's `docs/` stays game-focused (`plan.md`, `state.md`); content-engine's `docs/` holds content-pipeline planning.

- **Non-numbered DEVLOG entry, not "Day 6."** content-engine's day numbers track shipped code (Days 1–5: scaffold → DB → Reddit → YouTube → cross-poster pivot). Today is content-strategy work, not code. Same convention as DMS's content-planning entry handling: planning sessions get dated headers, not numbered ones, so the dev day count stays comparable.

- **5 player / 5 dev split, not weighted toward dev.** Dev material is stronger right now — concrete bugs, decisions, code. Player material is weaker but matters more long-term for actual user growth. Forcing equal coverage prevents the trap of only making clips about what's already easy to capture, which would lock the brand into "tutorials for other devs" with no path to actual players.

- **Loadout reveal is slot 01, not the Phase 1 recap.** A week-one account has no audience for a recap to compress for. The strongest scroll-stopper has to land first because algorithmic surfacing favors recent uploads, and "more from this account" pulls clip 01 forward when a stranger discovers any other clip in the rotation.

- **The whiff bug clip is non-negotiable, mid-rotation (slot 5).** Faceless dev accounts that show only polished wins lose trust within the first ten clips. One "here's what's still broken" slot — not at the start (sets the wrong tone) and not at the end (looks like an apology) — buys credibility for everything that surrounds it.

- **Captions stay platform-agnostic in `clips.md`.** The per-platform rewrite (TikTok hashtag count vs IG vs X length limits vs Shorts pinned-comment style) is the `caption draft` command's job — currently a stub but the next vertical slice. Drafting platform-specific captions here would force a rewrite when that command lands.

- **The audit was the most-valuable hour of the session.** Two clips had wrong premises (one caption inverted, one entire clip false), one had a "before" version that never existed, two oversold their visuals — none of which would have been caught without reading DMS source against the spec. Lesson: a content plan written from devlog notes alone is a draft. Audit before recording, always.

### What's intentionally not built yet

- **The recording session itself.** Planned for Sunday, ~2 hours, all 10 clips' raw material captured in one batch in DMS. Detailed plan in `docs/clips.md`. Two clips need temporarily-restored or written-from-scratch code in DMS (camera-shake bad version, kick whiff with sound); budget ~30 min round-trip overhead.
- **Editing pipeline.** Each clip needs an edit pass after capture — cyan/violet overlay text, MiggyDev corner mark, voiceover layered where applicable. Should happen on a separate day from recording.
- **`caption draft` command.** Still stubbed (Day 5). The clip plan is the input it'll consume — building the captioner is the next vertical slice once Sunday's recording lands raw material.
- **`metrics` group commands.** All stubbed. Not blocked by clip planning; sequenced after `caption draft` and `schedule`.

### Blockers for next session

- Sunday recording session needs ~2 uninterrupted hours and a quiet room for the three voiceover passes (whiff bug, victory, empty packet — ~30s combined audio).
- Two captures require temporarily-restored or written-from-scratch code in DMS (camera-shake bad version on a throwaway branch; whiff-bug pre-fix Kick effect call). Plan: `git stash` after capture in DMS, restore working tree before next dev day there.
- Re-evaluate `docs/clips.md` after recording. Splitter ban-spawning children (DMS Day 10) is genuinely strong clip material that the original 10-clip plan missed. Likely candidate to swap in for clip 09 (overlap with #04 as "tension" coverage), once a Sunday-recorded version of the original 10 exists for comparison.

### Hooks for the post

Pick one. Not all.

- **"Planning content for a faceless brand with zero audience"** — the constraints (faceless, low-key from the employer, 15–30s clips), the hard problem (week-one means strangers not followers), and the framework (player/dev split, hook-strength as ordering criterion). The strongest meta hook on this list.
- **"DEVLOG hooks are clip seeds"** — the workflow itself. The "Hooks for the post" section that the user's template forces at the bottom of every DEVLOG entry was already half-content; clipping it for video is one more transformation, and DEVLOG entries are the cheapest content-planning tool I have.
- **"Why the whiff bug clip is non-negotiable"** — authenticity math in a polish-heavy feed. The argument for one "here's what's broken" slot in every ten-clip rotation, and why slot 5 specifically.
- **"Choosing the loadout reveal over the recap as clip 01"** — content-strategy as a real engineering decision. The trade-off: a recap pays off only if the audience exists; a loadout reveal works on a stranger.
- **"Auditing your own content plan against the actual code"** — the meta-narrative that the audit itself was the most-valuable hour of this session. Two clips had wrong premises, one had a "before" version that never existed, two oversold their visuals — none of which would have been caught without reading the source against the spec. The lesson: a content plan written from devlog notes alone is a draft. Audit before recording, always.
- **"Where does the clip plan live? Not the game repo."** — the cross-repo correction. Putting `clips.md` in DMS coupled the two projects via a working doc; moving it to `content-engine` respects the integration-points rule (file-on-disk handoffs, each project owns its own concerns). Concrete example of refactoring an architectural mistake the day it happens.

---

## 2026-04-25 — Day 5: pivot to cross-poster

### What got built

- **Ripped 297 lines.** Old `scrapers/` (`reddit.py`, `youtube.py`), old `db/schema.sql` and `db/database.py` (`raw_posts` / `patterns` / `generated_content`), old `scrape` / `analyze` / `generate` / `query` commands in `main.py`. Removed `apscheduler` and `tweepy` from venv + `requirements.txt`. Stripped `REDDIT_USER_AGENT` and `APIFY_API_TOKEN` from `.env` and `.env.example`.
- **Archived, didn't delete:** `content.db` → `content.pre-pivot.db` (gitignored via `*.db`). 50 rows of real Reddit + YouTube data preserved as evidence the old pipeline worked end-to-end.
- **New schema, four tables.** `clips` (UNIQUE `file_path`), `captions` (no UNIQUE — multiple drafts per platform is the feature; token-tracking columns), `schedules` (UNIQUE `(clip_id, platform, scheduled_for)` + `CHECK (status IN ('queued', 'posted', 'failed'))`), `metrics` (no UNIQUE — time-series snapshots).
- **New `db/database.py`.** `init_db()`, `add_clip()` wired; `get_clip` / `add_caption` / `add_schedule` / `record_metric` / `list_schedules` raise `NotImplementedError` until their command lands.
- **New CLI: 7 commands across 5 groups.** `clip add` wired end-to-end. `caption draft`, `schedule`, `queue`, `metrics pull`, `metrics record`, `metrics show` are stubs that echo `(not implemented)`. `schedule` requires `--caption-id`. `metrics record` accepts `--at` for Sunday-batch backfill (defaults to now).
- **Three atomic commits**: `065564c` (rip), `2ea6314` (schema + DB), `4eb8693` (CLI + clip add). Smoke test passed: `clip add <test.mp4>` lands a row, re-register raises `ClickException`.
- **Docs rewritten** (this commit): `ROADMAP.md`, `CLAUDE.md`, `README.md` all replaced. DEVLOG-NOTES gets this Day 5 entry. Old docs described the dead pipeline — leaving them stale would have lied to the next Claude Code session.

### Decisions made (and why)

- **Pivot, not iterate.** The 6-week scrape → cluster → generate plan was solving the wrong problem for a faceless gamedev account. Algorithms suppress AI-generated text drafts; the actual bottleneck is "I don't have gameplay clips yet," not "I don't have ideas." Building a more sophisticated text-generation pipeline on top of that mistake would have compounded it. Rejected: keeping the old pipeline as "optional, in case I want it later" — two code paths means double the maintenance and ambient confusion.

- **Three commits, not one mega-commit.** A single "pivot to cross-poster" commit would have been honest but unrevertible at the slice level. Three atomic commits (rip / schema / CLI) means I can roll back any one independently. Same vertical-slice discipline as the scraper days.

- **Archive `content.db`, don't delete.** 50 real rows is evidence the old pipeline actually worked — useful for the "pivot" devlog post. Gitignored, costs nothing locally to keep.

- **`--caption-id` required on `schedule`, no implicit "latest".** Implicit "latest" bites at 11pm when three captions exist and the wrong one ships. Slightly worse typing for safety enforced at the CLI boundary instead of at the level of memory. Same energy as `INSERT OR IGNORE` over fetch-check-insert.

- **`CHECK (status IN ('queued', 'posted', 'failed'))` on `schedules`.** Schema-level constraint over Python flow control. Stops a typo'd `'posted '` (trailing space) from silently breaking `queue` filters two weeks from now.

- **Stubs raise `NotImplementedError`, not silent stub return.** Documents the eventual interface and forces a loud failure if a future command calls them too early.

- **Manual entry for TikTok / Instagram / X metrics is the design, not a temporary state.** TikTok has no public personal-account analytics API. Instagram needs Business + Meta Graph. X requires the $100/mo Basic tier. `metrics pull` docstring and `CLAUDE.md` sharp-edges section both spell this out so future-me doesn't burn a session trying to "fix" the autopull gap.

- **`--at` flag on `metrics record` defaults to now.** Five-minute add saves real friction — Sunday batch backfill is the realistic workflow, not entering snapshots at the moment you check each platform.

- **Aspect-ratio info is a printed checklist, not a schema column.** The MP4 has the ratio baked in when recorded; what's actually needed is a per-platform reminder ("TikTok: 9:16, ≤60s") at `schedule` time. Constant in code, not data.

- **Docs written *with* the code, not after.** Stale docs lie to the next Claude Code session and to a fresh hand-off. Rewriting `ROADMAP.md`, `CLAUDE.md`, `README.md` now (Commit D) is the same discipline as committing the smoke test alongside the feature.

### What's intentionally not built yet

- All commands except `clip add` — each is a future vertical slice. Next: `caption draft`.
- **Thumbnails** — struck from the goals list, not deferred. Different scope, image-gen cost is nontrivial, and Shorts/Reels autoplay in feed (custom thumbs rarely move the needle).
- `ffprobe` auto-detect for clip duration — manual `--duration` flag is fine for personal scale.
- Buffer / Publer / cross-posting service integration — defer until manual upload friction is real.
- TikTok / Instagram / X auto-pull metrics — design constraint (above), not a TODO.

### Blockers for next session

- `ANTHROPIC_API_KEY` in `.env` (currently empty) before `caption draft` can do anything live.
- Open prompt-design question: per-platform hook style varies a lot (TikTok ≠ Twitter). Resolve when we sketch the caption prompt.

### Hooks for the post

Pick one. Not all.

- **"The moment I realized I was building a content factory, not a tool"** — meta-narrative on the pivot. The bottleneck framing, the realization, the deletion. By far the strongest hook on this list — pivot stories perform well, and "I deleted 297 lines because the premise was wrong" is the kind of post other indie devs share.
- **"Ripping 297 lines is a feature"** — short, pointed post on the value of deletion when discovery beats continued investment. Useful for anyone afraid of throwing away work.
- **"The bottleneck wasn't ideas, it was clips"** — diagnostic post on solo creator economics. Why faceless accounts grow from gameplay clips, not AI-generated text drafts, and what changed in my plan when I named the actual constraint.
- **"Pipelines that automate the wrong thing"** — broader essay-flavored post on tool design. Why automating a non-bottleneck makes the bottleneck worse.

---

## 2026-04-25 — Day 4: YouTube scraper, query command, README, master→main

### What got built

- **`scrapers/youtube.py`** — `fetch_trending_videos(query, max_results)` using YouTube Data API v3. Two-call: `search.list` to find videos by query, `videos.list` (batched by id) to pull engagement stats. Returns dicts shaped to match `raw_posts`. Quota cost per scrape: 101 units against 10k daily.
- **`main.py` updates** — `scrape` command got a `--query` flag and a wired YouTube branch alongside Reddit. `query` command rewired to call `db.database.get_posts` and print formatted `[score] title` + url lines.
- **`README.md`** — public-facing setup + credentials table + usage examples + project-state checklist. Distinct from `CLAUDE.md` (internal context).
- **`master` → `main` migration** — local rename, remote `main` pushed and default flipped on GitHub, remote `master` deleted. Repo is now `https://github.com/MiggyDev619/content-engine` (public) on `main`.
- **Verified end-to-end** — `query --top 5 --source reddit` returned five real rows from yesterday's r/gamedev scrape. `scrape --source youtube` without `--query` errors cleanly. `scrape --source all` without flags skips both real sources gracefully.
- **YouTube live-verified** — `YOUTUBE_API_KEY` set (Google Cloud project, key restricted to YouTube Data API v3 only). `scrape --source youtube --query "roblox game dev" --limit 25` landed 25 rows; rerun deduped to 0. DB now holds 25 reddit + 25 youtube.
- **Two bugs surfaced and fixed during live verification:**
  - `UnicodeEncodeError` on emoji titles. Windows' default cp1252 stdout codec couldn't encode characters like `😱` / `💀` / `😹` that YouTube titles routinely contain. Fix: `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` at the top of `main.py`. One line, fixes everything downstream.
  - HTML-entity-encoded titles from YouTube. `Exposing Roblox&#39;s Richest Player` instead of `Exposing Roblox's Richest Player`. Fix: `html.unescape()` on `title` and `description` in `scrapers/youtube.py`. Cleared the 25 dirty youtube rows and re-scraped clean.

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

- None on the code side. Phase 1 multi-source scrape is 2 of 3 done (Reddit + YouTube live).
- Optional: Apify account if user wants to start TikTok scraping (Day 5–7 scope).
- Open question: mixed-source `query` ranks YouTube views above Reddit upvotes on the same `likes` column — needs a per-source ranking or normalized score before it's useful for cross-platform analysis. Defer until the analyzer needs it.

### Hooks for the post

Pick one. Not all.

- **"YouTube's API needs two calls to tell you what trended"** — `search.list` + `videos.list`, why the API design forces this split, and the 100+1 quota cost. Specific technical lesson, useful to anyone building media analytics.
- **"Why my Click parameter is named `query_`"** — two-paragraph mini-post on a name collision between a CLI subcommand and one of its options. Concrete, fixable, easy to understand.
- **"Renaming `master` → `main` on a four-day-old repo"** — quick-win post. Four commands, why now is cheaper than later, the gh-not-on-PATH gotcha.
- **"README is for humans; `CLAUDE.md` is for Claude"** — meta post on splitting public-facing docs from AI-context docs in a project that's actively used by Claude Code. Niche but interesting to anyone running AI-assisted dev workflows.
- **"Two bugs you hit the second your data has emoji and apostrophes"** — Windows cp1252 stdout vs `😱`, and YouTube returning `&#39;` instead of `'`. Both one-line fixes, both surfaced within 30 seconds of running the first live scrape. Concrete, useful, evergreen.

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

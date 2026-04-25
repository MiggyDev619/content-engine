import sys

import click
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()


@click.group()
def cli():
    """content-engine: record once, post everywhere, track everything."""


# -- clips -----------------------------------------------------------------

@cli.group()
def clip():
    """Manage recorded clips."""


@clip.command("add")
@click.argument("file_path", type=click.Path(exists=True, dir_okay=False, resolve_path=True))
@click.option("--title", required=True)
@click.option("--notes", default="", help="Free-form notes about what's in the clip")
@click.option("--duration", "duration_seconds", type=int, default=None,
              help="Clip length in seconds (manual; ffprobe auto-detect is a Phase 2 nice-to-have)")
@click.option("--recorded-at", "recorded_at", default=None,
              help='When the clip was recorded ("YYYY-MM-DD HH:MM"). Defaults to NULL.')
def clip_add(file_path, title, notes, duration_seconds, recorded_at):
    """Register a recorded clip in the DB."""
    from db.database import init_db, add_clip

    init_db()
    row = add_clip(
        file_path=file_path,
        title=title,
        notes=notes,
        duration_seconds=duration_seconds,
        recorded_at=recorded_at,
    )
    if row is None:
        raise click.ClickException(f"clip already registered: {file_path}")
    click.echo(f"clip added: id={row['id']} title={row['title']!r}")
    click.echo(f"  path:     {row['file_path']}")
    if row.get("duration_seconds"):
        click.echo(f"  duration: {row['duration_seconds']}s")


# -- captions --------------------------------------------------------------

@cli.group()
def caption():
    """Generate captions and hooks for clips."""


@caption.command("draft")
@click.argument("clip_id", type=int)
@click.option("--platform",
              type=click.Choice(["tiktok", "youtube", "twitter", "instagram", "all"]),
              default="all")
def caption_draft(clip_id, platform):
    """Draft captions/hooks for a clip via Claude (Opus for hooks, Sonnet for reformat)."""
    click.echo(f"caption draft: clip_id={clip_id} platform={platform} (not implemented)")


# -- schedules + queue -----------------------------------------------------

@cli.command()
@click.argument("clip_id", type=int)
@click.option("--caption-id", "caption_id", type=int, required=True,
              help="Required: which caption to commit to. Implicit 'latest' bites at 11pm.")
@click.option("--platform", required=True,
              type=click.Choice(["tiktok", "youtube", "twitter", "instagram"]))
@click.option("--datetime", "scheduled_for", required=True,
              help='When to post: "YYYY-MM-DD HH:MM"')
def schedule(clip_id, caption_id, platform, scheduled_for):
    """Schedule a clip+caption for a platform at a specific time."""
    click.echo(
        f"schedule: clip_id={clip_id} caption_id={caption_id} "
        f"platform={platform} at={scheduled_for} (not implemented)"
    )


@cli.command()
def queue():
    """Show what's scheduled this week, per platform."""
    click.echo("queue: (not implemented)")


# -- metrics ---------------------------------------------------------------

@cli.group()
def metrics():
    """Pull and view per-platform analytics."""


@metrics.command("pull")
def metrics_pull():
    """Fetch analytics from each platform's API.

    \b
    Auto-pull (Day 2+):
      youtube — YouTube Data API + OAuth, free
    Manual entry (use `metrics record`):
      tiktok    — no public API for personal-account analytics
      instagram — needs Business account + Meta Graph
      twitter   — Basic tier ($100/mo), deferred
    """
    click.echo("metrics pull: (not implemented)")


@metrics.command("record")
@click.argument("schedule_id", type=int)
@click.option("--views", type=int, required=True)
@click.option("--likes", type=int, default=0)
@click.option("--comments", type=int, default=0)
@click.option("--shares", type=int, default=0)
@click.option("--at", "fetched_at", default=None,
              help='Snapshot timestamp ("YYYY-MM-DD HH:MM"). Defaults to now — '
                   'use this to backfill from a Sunday batch instead of being '
                   'forced to log at the moment you check.')
def metrics_record(schedule_id, views, likes, comments, shares, fetched_at):
    """Manually record a metrics snapshot for a scheduled post."""
    click.echo(
        f"metrics record: schedule_id={schedule_id} "
        f"views={views} likes={likes} comments={comments} shares={shares} "
        f"at={fetched_at or 'now'} (not implemented)"
    )


@metrics.command("show")
@click.option("--days", default=7, type=int)
def metrics_show(days):
    """One CLI table: clip title | platform | views | likes | comments. Last N days."""
    click.echo(f"metrics show: days={days} (not implemented)")


if __name__ == "__main__":
    cli()

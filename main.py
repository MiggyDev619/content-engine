import click
from dotenv import load_dotenv

load_dotenv()


@click.group()
def cli():
    """AI Content Distribution + Trend Analysis Engine."""


@cli.command()
@click.option("--source", type=click.Choice(["reddit", "youtube", "tiktok", "all"]), default="all")
@click.option("--subreddit", default=None, help="Subreddit (reddit only)")
@click.option("--query", "query_", default=None, help="Search query (youtube only)")
@click.option("--limit", default=25, type=int)
def scrape(source, subreddit, query_, limit):
    """Pull trending content from a source into the DB."""
    from db.database import init_db, insert_post

    init_db()

    if source in ("reddit", "all"):
        if not subreddit:
            if source == "reddit":
                raise click.ClickException("--subreddit is required for reddit source")
            click.echo("reddit: skipped (no --subreddit given)")
        else:
            from scrapers.reddit import fetch_top_posts
            posts = fetch_top_posts(subreddit, limit=limit)
            inserted = sum(1 for p in posts if insert_post(p))
            click.echo(f"reddit: scraped {len(posts)} from r/{subreddit}, {inserted} new rows")

    if source in ("youtube", "all"):
        if not query_:
            if source == "youtube":
                raise click.ClickException("--query is required for youtube source")
            click.echo("youtube: skipped (no --query given)")
        else:
            from scrapers.youtube import fetch_trending_videos
            posts = fetch_trending_videos(query_, max_results=limit)
            inserted = sum(1 for p in posts if insert_post(p))
            click.echo(f"youtube: scraped {len(posts)} for q={query_!r}, {inserted} new rows")

    if source in ("tiktok", "all"):
        click.echo("tiktok: not implemented yet")


@cli.command()
@click.option("--limit", default=50, type=int)
def analyze(limit):
    """Send scraped posts to Claude and extract patterns."""
    click.echo(f"analyze: limit={limit} (not implemented)")


@cli.command()
@click.option("--topic", required=True)
@click.option("--platform", type=click.Choice(["tiktok", "youtube", "twitter", "instagram", "all"]), default="all")
def generate(topic, platform):
    """Generate platform-specific content drafts."""
    click.echo(f"generate: topic={topic!r} platform={platform} (not implemented)")


@cli.command()
@click.option("--top", default=20, type=int)
@click.option("--source", default=None, type=click.Choice(["reddit", "youtube", "tiktok"]))
def query(top, source):
    """Print top posts from the DB ordered by likes desc."""
    from db.database import get_posts

    posts = get_posts(source=source, limit=top)
    if not posts:
        click.echo("(no posts)")
        return
    for p in posts:
        score = p.get("likes") or 0
        title = (p.get("title") or "").strip()
        url = p.get("url") or ""
        click.echo(f"[{score:>5}] {title[:80]}")
        click.echo(f"        {url}")


if __name__ == "__main__":
    cli()

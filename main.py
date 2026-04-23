import click
from dotenv import load_dotenv

load_dotenv()


@click.group()
def cli():
    """AI Content Distribution + Trend Analysis Engine."""


@cli.command()
@click.option("--source", type=click.Choice(["reddit", "youtube", "tiktok", "all"]), default="all")
@click.option("--subreddit", default=None, help="Subreddit to pull from (reddit only)")
@click.option("--limit", default=25, type=int)
def scrape(source, subreddit, limit):
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
        click.echo("youtube: not implemented yet")

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
@click.option("--source", default=None)
def query(top, source):
    """Print top posts from the DB by engagement."""
    click.echo(f"query: top={top} source={source} (not implemented)")


if __name__ == "__main__":
    cli()

import sys

import click
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()


@click.group()
def cli():
    """content-engine: record once, post everywhere, track everything."""


if __name__ == "__main__":
    cli()

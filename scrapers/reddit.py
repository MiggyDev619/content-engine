import os

import praw


def _client() -> praw.Reddit:
    return praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ.get("REDDIT_USER_AGENT", "content-engine"),
    )


def fetch_top_posts(subreddit: str, limit: int = 25, time_filter: str = "day") -> list[dict]:
    """Fetch top submissions from a subreddit.

    Returns dicts shaped to match the raw_posts schema. `time_filter` is one of
    'hour', 'day', 'week', 'month', 'year', 'all'.
    """
    reddit = _client()
    posts: list[dict] = []
    for s in reddit.subreddit(subreddit).top(time_filter=time_filter, limit=limit):
        posts.append({
            "source": "reddit",
            "external_id": s.id,
            "title": s.title,
            "description": s.selftext or "",
            "url": s.url,
            "author": str(s.author) if s.author else None,
            "likes": s.score,
            "comments": s.num_comments,
            "views": 0,
            "shares": 0,
        })
    return posts

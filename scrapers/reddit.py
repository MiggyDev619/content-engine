import os

import httpx

REDDIT_BASE = "https://www.reddit.com"


def fetch_top_posts(subreddit: str, limit: int = 25, time_filter: str = "day") -> list[dict]:
    """Fetch top submissions from a subreddit via Reddit's public JSON endpoint.

    No OAuth — Reddit's Responsible Builder Policy gates self-serve script apps,
    so we hit the public JSON endpoint and rely on a descriptive User-Agent.
    `time_filter` is one of 'hour', 'day', 'week', 'month', 'year', 'all'.
    """
    ua = os.environ.get("REDDIT_USER_AGENT", "content-engine/0.1")
    url = f"{REDDIT_BASE}/r/{subreddit}/top.json"
    params = {"t": time_filter, "limit": limit}
    headers = {"User-Agent": ua}

    resp = httpx.get(url, params=params, headers=headers, timeout=10.0)
    resp.raise_for_status()
    data = resp.json()

    posts: list[dict] = []
    for child in data["data"]["children"]:
        s = child["data"]
        posts.append({
            "source": "reddit",
            "external_id": s["id"],
            "title": s.get("title", ""),
            "description": s.get("selftext", "") or "",
            "url": s.get("url", ""),
            "author": s.get("author"),
            "likes": int(s.get("score", 0) or 0),
            "comments": int(s.get("num_comments", 0) or 0),
            "views": 0,
            "shares": 0,
        })
    return posts

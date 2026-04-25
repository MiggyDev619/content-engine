import os
from html import unescape

import httpx

YT_BASE = "https://www.googleapis.com/youtube/v3"


def fetch_trending_videos(query: str, max_results: int = 25) -> list[dict]:
    """Fetch top videos for a query via YouTube Data API v3.

    Two-step call: search.list to find videos by query, then videos.list to
    pull engagement statistics (search.list doesn't return view/like counts).
    Returns dicts shaped to match the raw_posts schema.
    """
    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        raise RuntimeError("YOUTUBE_API_KEY not set in .env")

    # search.list — costs 100 quota units. API caps maxResults at 50.
    search = httpx.get(
        f"{YT_BASE}/search",
        params={
            "key": api_key,
            "part": "snippet",
            "q": query,
            "type": "video",
            "order": "viewCount",
            "maxResults": min(max_results, 50),
        },
        timeout=10.0,
    )
    search.raise_for_status()
    items = search.json().get("items", [])
    if not items:
        return []

    # videos.list — costs 1 quota unit, batched for all ids in one call.
    video_ids = [item["id"]["videoId"] for item in items]
    stats_resp = httpx.get(
        f"{YT_BASE}/videos",
        params={"key": api_key, "part": "statistics", "id": ",".join(video_ids)},
        timeout=10.0,
    )
    stats_resp.raise_for_status()
    stats_by_id = {v["id"]: v.get("statistics", {}) for v in stats_resp.json().get("items", [])}

    posts: list[dict] = []
    for item in items:
        vid = item["id"]["videoId"]
        snippet = item["snippet"]
        stats = stats_by_id.get(vid, {})
        posts.append({
            "source": "youtube",
            "external_id": vid,
            "title": unescape(snippet.get("title", "")),
            "description": unescape(snippet.get("description", "")),
            "url": f"https://www.youtube.com/watch?v={vid}",
            "author": snippet.get("channelTitle"),
            "likes": int(stats.get("likeCount", 0) or 0),
            "comments": int(stats.get("commentCount", 0) or 0),
            "views": int(stats.get("viewCount", 0) or 0),
            "shares": 0,
        })
    return posts

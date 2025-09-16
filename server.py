# server.py — Minimal MCP server for YouTube comments (STDIO)
from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP
import httpx, os, re, json, logging
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
mcp = FastMCP("yt_comments")

load_dotenv()
YT_API_KEY = os.environ.get("YOUTUBE_API_KEY")
YT_BASE = "https://www.googleapis.com/youtube/v3"

def _extract_video_id(video_url: str) -> str:
    """Support https://www.youtube.com/watch?v=..., https://youtu.be/..., /embed/..."""
    try:
        u = urlparse(video_url)
        if u.netloc.endswith("youtu.be"):
            return u.path.strip("/")
        if "youtube.com" in u.netloc:
            qs = parse_qs(u.query or "")
            if "v" in qs:
                return qs["v"][0]
            m = re.search(r"/embed/([A-Za-z0-9_-]{6,})", u.path or "")
            if m:
                return m.group(1)
        m = re.search(r"([A-Za-z0-9_-]{11})", video_url)
        return m.group(1) if m else ""
    except Exception:
        return ""

async def _yt_get(client: httpx.AsyncClient, path: str, params: Dict[str, Any]) -> Dict[str, Any]:
    params = dict(params); params["key"] = YT_API_KEY
    r = await client.get(f"{YT_BASE}/{path}", params=params, timeout=30.0)
    r.raise_for_status()
    return r.json()

def _pack_comment(item: Dict[str, Any], parent_id: Optional[str] = None) -> Dict[str, Any]:
    s = item.get("snippet", {})
    return {
        "id": item.get("id"),
        "parentId": parent_id,
        "author": s.get("authorDisplayName"),
        "publishedAt": s.get("publishedAt"),
        "likeCount": s.get("likeCount", 0),
        "text": s.get("textOriginal") or s.get("textDisplay") or "",
    }

@mcp.tool()
async def fetch_comments(videoUrl: str, order: str = "relevance", max: int = 300) -> str:
    """
    Fetch public comments for a YouTube video and return a JSON string.
    Args:
      videoUrl: Full YouTube video URL.
      order: "relevance" (default) or "time".
      max: Max total comments to return (100–1000 建議).
    """
    if not os.environ.get("YOUTUBE_API_KEY"):
        return "ERROR: Missing YOUTUBE_API_KEY in environment."
    video_id = _extract_video_id(videoUrl)
    if not video_id:
        return "ERROR: Cannot parse video ID from URL."
    order = order if order in ("relevance", "time") else "relevance"

    items: List[Dict[str, Any]] = []
    page_token = None
    try:
        async with httpx.AsyncClient() as client:
            while True:
                params = {
                    "part": "snippet,replies",
                    "videoId": video_id,
                    "maxResults": 100,
                    "order": order,
                    "textFormat": "plainText",
                }
                if page_token:
                    params["pageToken"] = page_token
                data = await _yt_get(client, "commentThreads", params)

                for th in data.get("items", []):
                    top = th.get("snippet", {}).get("topLevelComment", {})
                    if top:
                        items.append(_pack_comment(top))
                    for rep in th.get("replies", {}).get("comments", []) or []:
                        items.append(_pack_comment(rep, parent_id=top.get("id") if top else None))

                    if len(items) >= max:
                        break
                if len(items) >= max:
                    break
                page_token = data.get("nextPageToken")
                if not page_token:
                    break

        return json.dumps({
            "video_id": video_id,
            "order": order,
            "requested": max,
            "total_returned": len(items),
            "items": items
        }, ensure_ascii=False)
    except httpx.HTTPStatusError as e:
        return f"ERROR: HTTP {e.response.status_code} – {e.response.text}"
    except Exception as e:
        return f"ERROR: {type(e).__name__}: {e}"

if __name__ == "__main__":
    # Claude Desktop / Inspector 透過 STDIO 連線
    mcp.run(transport="stdio")

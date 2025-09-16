
# yt_mcp — YouTube Comments MCP Server

一個遵循 **Model Context Protocol (MCP)** 的本機伺服器，提供工具：
- `fetch_comments(videoUrl, order="relevance|time", max=300)`  
  回傳展開的 YouTube 頂層留言＋回覆（JSON 字串）。


---

## 安裝

```bash
uv venv
source .venv/bin/activate
uv pip install "mcp[cli]" httpx python-dotenv


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
在 Claude Desktop 使用（本機 STDIO）
Settings → Developer → Local MCP servers → Edit Config，加入（請換成你的絕對路徑）：
{
  "mcpServers": {
    "yt_comments": {
      "command": "<abs path>/yt_mcp/.venv/bin/python",
      "args": ["<abs path>/yt_mcp/server.py"],
      "env": { "YOUTUBE_API_KEY": "YOUR_API_KEY" }
    }
  }
}
你也可移除 env，改用專案根目錄的 .env。
回到 Local MCP servers 啟動 yt_comments。
新開對話，請 Claude 呼叫：
yt_comments.fetch_comments(
  videoUrl="https://www.youtube.com/watch?v=XXXXXXXXXXX",
  order="relevance",
  max=300
)
然後讓模型做摘要/分類/翻譯並輸出報告。
在 MCP Inspector 測試
Transport: STDIO
Command: <abs path>/yt_mcp/.venv/bin/python
Arguments: server.py
（可選）Environment: YOUTUBE_API_KEY=<你的金鑰>
輸出格式（節選）
{
  "video_id": "abcdEFGhijk",
  "order": "relevance",
  "requested": 300,
  "total_returned": 278,
  "items": [
    {
      "id": "...",
      "parentId": null,
      "author": "Somebody",
      "publishedAt": "2025-01-01T12:34:56Z",
      "likeCount": 42,
      "text": "Great video!"
    }
  ]
}
Troubleshooting
Missing YOUTUBE_API_KEY：在 .env 或設定的 env 補上金鑰，並確保金鑰已啟用 YouTube Data API v3。
找不到 server.py：在 Claude 的設定用 絕對路徑 放到 "args"。
ModuleNotFoundError：確認已在 venv 內安裝相依套件。
403/400：配額不足、影片關閉留言、或金鑰權限未開。
安全
.env 已被 .gitignore 排除；請勿提交金鑰。
若曾不小心提交金鑰，請旋轉金鑰並清理 Git 歷史。

---

如果你要一份 **MIT License** 我也可以幫你生成；或想把「一鍵產 Markdown 報告」做成第二個工具 `export_report`，我能再補上相對應的程式碼。
::contentReference[oaicite:0]{index=0}

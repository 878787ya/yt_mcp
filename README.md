---

# yt\_mcp — YouTube Comments MCP Server

一個遵循 **Model Context Protocol (MCP)** 的本機伺服器。提供工具：

* `fetch_comments(videoUrl, order="relevance|time", max=300)`
  以 YouTube Data API v3 取得並展開 **頂層留言＋回覆**，回傳 **JSON 字串**。

---

## 需求

* Python 3.10+
* 已啟用 **YouTube Data API v3** 的 API 金鑰

---

## 安裝

```bash
uv venv
source .venv/bin/activate
uv pip install "mcp[cli]" httpx python-dotenv
```

### 設定金鑰（擇一）

**A. 用 `.env`（推薦）**

在專案根目錄建立 `.env`：

```
YOUTUBE_API_KEY=YOUR_API_KEY_HERE
```

**B. 寫在客戶端設定的 `env`（見下方範例）**

---

## 在 Claude Desktop 使用（本機 STDIO）

1. 開啟：**Settings → Developer → Local MCP servers → Edit Config**
2. 加入（請把絕對路徑換成你的實際路徑）：

```json
{
  "mcpServers": {
    "yt_comments": {
      "command": "<abs path>/yt_mcp/.venv/bin/python",
      "args": ["<abs path>/yt_mcp/server.py"],
      "env": { "YOUTUBE_API_KEY": "YOUR_API_KEY" }  // 若已用 .env，可移除此段
    }
  }
}
```

> 也可不填 `env`，改用專案根目錄的 `.env`。

3. 回到 **Local MCP servers** 啟動 `yt_comments`。
4. 新開對話請 Claude 呼叫：

```text
yt_comments.fetch_comments(
  videoUrl="https://www.youtube.com/watch?v=XXXXXXXXXXX",
  order="relevance",
  max=300
)
```

接著請模型做摘要／分類／翻譯並輸出報告。

---

## 在 MCP Inspector 測試

* **Transport**：`STDIO`
* **Command**：`<abs path>/yt_mcp/.venv/bin/python`
* **Arguments**：`<abs path>/yt_mcp/server.py`
* **Environment（可選）**：`YOUTUBE_API_KEY=YOUR_API_KEY`

---

## 輸出格式（節選）

```json
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
```

---

## Troubleshooting

* **Missing YOUTUBE\_API\_KEY**
  在 `.env` 或設定的 `env` 補上金鑰，並確認金鑰已啟用 **YouTube Data API v3**。
* **找不到 `server.py`**
  在設定裡把 **`args` 改用絕對路徑**（例如 `"/Users/you/yt_mcp/server.py"`）。
* **ModuleNotFoundError**
  確認已在虛擬環境內安裝相依套件（`"mcp[cli]" httpx python-dotenv`）。
* **HTTP 403/400**
  可能是配額不足、影片關閉留言、或金鑰權限未開。

---

## 安全

* `.env` 已在 `.gitignore` 中，**請勿**提交金鑰。
* 若曾不小心提交金鑰，請 **旋轉金鑰** 並清理 Git 歷史。

---

## 授權

**MIT License**。


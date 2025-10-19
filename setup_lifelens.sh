#!/usr/bin/env bash
set -e
ROOT="/workspaces/known-history/lifelens-ai"
echo "Creating project at $ROOT"
mkdir -p "$ROOT"/{extension/popup,webapp,backend,docs,demo}
mkdir -p "$ROOT/webapp/src/components" "$ROOT/backend/services"
# (minimal files)
cat > "$ROOT/extension/manifest.json" <<'JSON'
{
  "manifest_version": 3,
  "name": "LifeLens AI",
  "version": "0.1.0",
  "description": "Privacy-first page summarizer & semantic history",
  "permissions": ["storage", "scripting", "activeTab"],
  "host_permissions": ["<all_urls>"],
  "background": { "service_worker": "background.js" },
  "action": { "default_popup": "popup/index.html" },
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content.js"],
      "run_at": "document_end"
    }
  ]
}
JSON
cat > "$ROOT/extension/content.js" <<'EOF'
(() => {
  const snippet = (document.body && document.body.innerText) ? document.body.innerText.slice(0,3000) : '';
  console.log('LifeLens capture', { url: location.href, title: document.title, snippet_len: snippet.length });
})();
EOF
cat > "$ROOT/backend/app.py" <<'EOF'
from fastapi import FastAPI
app = FastAPI()
@app.get("/health")
async def health(): return {"status":"ok"}
EOF
cat > "$ROOT/webapp/index.html" <<'EOF'
<!doctype html><html><head><meta charset="utf-8"/><title>LifeLens</title></head><body><h1>Dashboard</h1></body></html>
EOF
cat > "$ROOT/.env.example" <<'EOF'
GEMINI_API_KEY=
AUTH0_DOMAIN=
AUTH0_CLIENT_ID=
SNOWFLAKE_ACCOUNT=
DO_API_TOKEN=
EOF
echo "done"

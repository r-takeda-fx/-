---
description: ローカルサーバーを起動してアプリを確認
---

# プロジェクト実行

## ローカル確認方法

### 方法1: VS Code Live Server
1. VS Codeで `index.html` を開く
2. 右クリック → "Open with Live Server"

### 方法2: Python HTTP Server
```bash
cd ~/.claude/projects/consulting-ai-news
python -m http.server 8000
```
→ http://localhost:8000 でアクセス

### 方法3: Node.js (npx)
```bash
cd ~/.claude/projects/consulting-ai-news
npx serve
```

## 確認ポイント
- [ ] タブ切り替えが動作するか
- [ ] スマホ表示（DevToolsでモバイルビュー）
- [ ] ニュースが正しく表示されるか

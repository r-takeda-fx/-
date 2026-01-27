# 再利用パターン集（Patterns）

プロジェクトで使用する/発見したパターンを記録します。

---

## P1: タブ切り替えパターン

**カテゴリ**: コード

### 使用場面
コンテンツをタブで切り替えて表示する場合

### パターン
```javascript
// タブボタンにdata属性でターゲットを指定
// <button data-tab="consulting">コンサル</button>
// <div id="consulting" class="tab-content">...</div>

document.querySelectorAll('[data-tab]').forEach(button => {
  button.addEventListener('click', () => {
    const target = button.dataset.tab;
    // 全タブを非表示
    document.querySelectorAll('.tab-content').forEach(content => {
      content.classList.remove('active');
    });
    // ターゲットを表示
    document.getElementById(target).classList.add('active');
    // ボタンのアクティブ状態を更新
    document.querySelectorAll('[data-tab]').forEach(btn => {
      btn.classList.remove('active');
    });
    button.classList.add('active');
  });
});
```

### 注意点
- アクセシビリティ対応（role="tablist", aria-selected等）を検討

---

## P2: レスポンシブカードレイアウト

**カテゴリ**: CSS

### 使用場面
ニュース記事をカード形式で表示する場合

### パターン
```css
.news-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  padding: 1rem;
}

.news-card {
  background: white;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
```

### 注意点
- minmaxの最小値はスマホ画面幅を考慮

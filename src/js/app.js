/**
 * コンサル業界・AI最新ニュースアプリ
 * タブ切り替えとニュース表示機能
 */

// ========================================
// サンプルニュースデータ
// ========================================

/**
 * コンサル業界ニュース
 */
const consultingNews = [
    {
        title: "マッキンゼー、生成AIを活用した経営コンサルティングサービスを本格展開",
        source: "日本経済新聞",
        date: "2026-01-27",
        summary: "マッキンゼー・アンド・カンパニーは、生成AIを活用した新たな経営コンサルティングサービス「Lilli」の日本市場での本格展開を発表。企業のDX推進を加速させる。",
        url: "https://example.com/mckinsey-ai"
    },
    {
        title: "BCG、サステナビリティ領域の専門チームを大幅増強",
        source: "東洋経済オンライン",
        date: "2026-01-26",
        summary: "ボストン・コンサルティング・グループは、ESG・サステナビリティ分野の専門コンサルタントを2026年中に50%増員する計画を発表。脱炭素経営支援の需要増に対応。",
        url: "https://example.com/bcg-sustainability"
    },
    {
        title: "デロイト トーマツ、M&Aアドバイザリー部門が過去最高の売上を記録",
        source: "週刊ダイヤモンド",
        date: "2026-01-25",
        summary: "デロイト トーマツ ファイナンシャルアドバイザリーは、2025年度のM&Aアドバイザリー売上高が過去最高を更新したと発表。事業承継案件の増加が寄与。",
        url: "https://example.com/deloitte-ma"
    },
    {
        title: "アクセンチュア、日本でのDX人材を5,000人規模に拡大へ",
        source: "ITmedia",
        date: "2026-01-24",
        summary: "アクセンチュアは2027年までに日本国内のDX専門人材を5,000人規模に拡大する方針を明らかにした。クラウド移行とAI導入支援の需要増に対応。",
        url: "https://example.com/accenture-dx"
    },
    {
        title: "PwC、スタートアップ向け成長支援プログラムを刷新",
        source: "Forbes Japan",
        date: "2026-01-23",
        summary: "PwC Japanグループは、スタートアップ企業向けの成長支援プログラム「Scale-Up Academy」を刷新。IPO準備からグローバル展開まで一気通貫で支援。",
        url: "https://example.com/pwc-startup"
    }
];

/**
 * AI関連ニュース
 */
const aiNews = [
    {
        title: "OpenAI、GPT-5の開発状況を公開 - 推論能力が大幅向上",
        source: "TechCrunch Japan",
        date: "2026-01-27",
        summary: "OpenAIは次期大規模言語モデル「GPT-5」の開発進捗を公開。複雑な推論タスクにおいて人間の専門家レベルの性能を達成したと発表。",
        url: "https://example.com/gpt5"
    },
    {
        title: "Anthropic、Claude 4.5をリリース - 長文理解と多言語対応を強化",
        source: "WIRED Japan",
        date: "2026-01-26",
        summary: "Anthropicは最新AIアシスタント「Claude 4.5」をリリース。20万トークンのコンテキスト長と100以上の言語サポートを実現し、ビジネス用途での採用が加速。",
        url: "https://example.com/claude-45"
    },
    {
        title: "Google、Gemini 2.0を発表 - マルチモーダル性能で業界最高水準",
        source: "Impress Watch",
        date: "2026-01-25",
        summary: "Googleは次世代AIモデル「Gemini 2.0」を発表。画像・動画・音声の統合理解において業界最高水準の性能を達成。Google Workspaceへの統合も強化。",
        url: "https://example.com/gemini-2"
    },
    {
        title: "EU AI規制法が施行開始 - 生成AIに厳格な透明性要件",
        source: "日経クロステック",
        date: "2026-01-24",
        summary: "EU AI法（EU AI Act）の主要規定が施行開始。生成AIシステムには学習データの開示義務やコンテンツのAI生成表示が義務化される。",
        url: "https://example.com/eu-ai-act"
    },
    {
        title: "日本政府、AI戦略2026を策定 - 国産LLM開発に1,000億円投資",
        source: "NHKニュース",
        date: "2026-01-23",
        summary: "政府は「AI戦略2026」を閣議決定。国産大規模言語モデルの開発に1,000億円を投資し、産学官連携による国際競争力強化を目指す。",
        url: "https://example.com/japan-ai-strategy"
    }
];

// ========================================
// タブ切り替え機能
// ========================================

/**
 * タブ切り替えを初期化
 * data-tab属性でターゲットを指定し、クリックで対応するタブを表示
 */
function initTabs() {
    const tabButtons = document.querySelectorAll('.tabs__button[data-tab]');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetId = button.getAttribute('data-tab');

            // 全てのタブボタンのactive状態とaria-selectedを解除
            tabButtons.forEach(btn => {
                btn.classList.remove('active');
                btn.setAttribute('aria-selected', 'false');
            });

            // 全てのタブコンテンツを非表示
            tabPanes.forEach(pane => {
                pane.classList.remove('active');
            });

            // クリックされたボタンをactive状態に
            button.classList.add('active');
            button.setAttribute('aria-selected', 'true');

            // 対応するタブコンテンツを表示
            const targetPane = document.getElementById(targetId);
            if (targetPane) {
                targetPane.classList.add('active');
            }
        });
    });
}

// ========================================
// ニュース表示機能
// ========================================

/**
 * ニュースカードのHTML文字列を生成
 * @param {Object} news - ニュースオブジェクト
 * @returns {string} - ニュースカードのHTML
 */
function createNewsCardHTML(news) {
    return `
        <article class="news-card" ${news.url ? `data-url="${news.url}"` : ''}>
            <h3 class="news-card__title">${escapeHTML(news.title)}</h3>
            <div class="news-card__meta">
                <span class="news-card__source">${escapeHTML(news.source)}</span>
                <span class="news-card__date">${escapeHTML(news.date)}</span>
            </div>
            <p class="news-card__summary">${escapeHTML(news.summary)}</p>
        </article>
    `;
}

/**
 * HTMLエスケープ処理
 * XSS対策のため、特殊文字をエスケープ
 * @param {string} text - エスケープ対象の文字列
 * @returns {string} - エスケープ後の文字列
 */
function escapeHTML(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * 指定されたコンテナにニュースを表示
 * @param {string} containerId - ニュースを表示するコンテナのID
 * @param {Array} newsArray - ニュースオブジェクトの配列
 */
function renderNews(containerId, newsArray) {
    const container = document.getElementById(containerId);
    if (!container) {
        console.error(`コンテナが見つかりません: ${containerId}`);
        return;
    }

    // ニュースカードのHTMLを生成して挿入
    const newsHTML = newsArray.map(news => createNewsCardHTML(news)).join('');
    container.innerHTML = newsHTML;

    // カードクリックイベントを設定
    const newsCards = container.querySelectorAll('.news-card[data-url]');
    newsCards.forEach(card => {
        card.style.cursor = 'pointer';
        card.addEventListener('click', () => {
            const url = card.getAttribute('data-url');
            if (url) {
                window.open(url, '_blank', 'noopener,noreferrer');
            }
        });
    });
}

// ========================================
// 初期化
// ========================================

/**
 * アプリケーションの初期化
 * DOM読み込み完了後に実行
 */
function initApp() {
    // タブ切り替え機能を初期化
    initTabs();

    // 両カテゴリのニュースを表示
    renderNews('consulting-news', consultingNews);
    renderNews('ai-news', aiNews);
}

// DOMContentLoaded時に初期化を実行
document.addEventListener('DOMContentLoaded', initApp);

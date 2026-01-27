#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RSSフィードからニュースを取得し、カテゴリ別にJSON保存するスクリプト

機能:
- コンサル業界とAIの2カテゴリのRSSフィードを取得
- 日付別のJSONファイルとして保存
- 最新7日分のみ保持（古いファイルは自動削除）
"""

import feedparser
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import TypedDict
from zoneinfo import ZoneInfo

# 日本時間タイムゾーン
JST = ZoneInfo("Asia/Tokyo")

# RSSフィード設定
RSS_FEEDS: dict[str, list[dict[str, str]]] = {
    "consulting": [
        {"name": "ITmedia ビジネス", "url": "https://rss.itmedia.co.jp/rss/2.0/bizid.xml"},
        {"name": "東洋経済オンライン", "url": "https://toyokeizai.net/list/feed/rss"},
    ],
    "ai": [
        {"name": "ITmedia AI+", "url": "https://rss.itmedia.co.jp/rss/2.0/aiplus.xml"},
        {"name": "GIGAZINE", "url": "https://gigazine.net/news/rss_2.0/"},
    ],
    "poker": [
        {"name": "PokerNews", "url": "https://www.pokernews.com/news.rss"},
        {"name": "Card Player", "url": "https://www.cardplayer.com/poker-news/rss"},
    ],
}

# 設定
MAX_ARTICLES_PER_CATEGORY = 10  # 各カテゴリの最大記事数
MAX_SUMMARY_LENGTH = 150  # 要約の最大文字数
KEEP_DAYS = 7  # 保持する日数
DATA_DIR = Path(__file__).parent.parent / "data"  # データ保存ディレクトリ


class Article(TypedDict):
    """記事の型定義"""
    title: str
    source: str
    date: str
    summary: str
    url: str


class NewsData(TypedDict):
    """ニュースデータの型定義"""
    date: str
    updated_at: str
    consulting: list[Article]
    ai: list[Article]
    poker: list[Article]


def truncate_text(text: str, max_length: int) -> str:
    """
    テキストを指定文字数で切り詰める

    Args:
        text: 元のテキスト
        max_length: 最大文字数

    Returns:
        切り詰めたテキスト（超過時は「...」を付加）
    """
    if not text:
        return ""

    # HTMLタグを簡易的に除去
    import re
    text = re.sub(r'<[^>]+>', '', text)
    # 改行・タブを空白に変換
    text = re.sub(r'[\n\r\t]+', ' ', text)
    # 連続する空白を1つに
    text = re.sub(r'\s+', ' ', text).strip()

    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def parse_date(entry: feedparser.FeedParserDict) -> str:
    """
    RSSエントリから日付を抽出

    Args:
        entry: feedparserのエントリ

    Returns:
        YYYY-MM-DD形式の日付文字列
    """
    # published_parsed または updated_parsed から日付を取得
    time_struct = entry.get("published_parsed") or entry.get("updated_parsed")

    if time_struct:
        dt = datetime(*time_struct[:6])
        return dt.strftime("%Y-%m-%d")

    # 日付が取得できない場合は今日の日付を使用
    return datetime.now(JST).strftime("%Y-%m-%d")


def fetch_feed(feed_config: dict[str, str]) -> list[Article]:
    """
    単一のRSSフィードから記事を取得

    Args:
        feed_config: フィード設定（name, url）

    Returns:
        記事のリスト
    """
    articles: list[Article] = []

    try:
        print(f"  フィード取得中: {feed_config['name']} ({feed_config['url']})")
        feed = feedparser.parse(feed_config["url"])

        # フィードのステータス確認
        if hasattr(feed, "status") and feed.status >= 400:
            print(f"    警告: HTTPステータス {feed.status}")
            return articles

        if feed.bozo and feed.bozo_exception:
            print(f"    警告: パースエラー - {feed.bozo_exception}")

        for entry in feed.entries:
            # 必須フィールドの確認
            if not entry.get("link"):
                continue

            # 要約の取得（summaryまたはdescription）
            summary = entry.get("summary", "") or entry.get("description", "")

            article: Article = {
                "title": entry.get("title", "タイトルなし"),
                "source": feed_config["name"],
                "date": parse_date(entry),
                "summary": truncate_text(summary, MAX_SUMMARY_LENGTH),
                "url": entry.link,
            }
            articles.append(article)

        print(f"    取得完了: {len(articles)}件")

    except Exception as e:
        print(f"    エラー: {feed_config['name']} - {e}")

    return articles


def fetch_category_news(category: str, feeds: list[dict[str, str]]) -> list[Article]:
    """
    カテゴリ内の全フィードから記事を取得（重複排除）

    Args:
        category: カテゴリ名
        feeds: フィード設定のリスト

    Returns:
        重複排除・件数制限済みの記事リスト
    """
    print(f"\n[{category}] カテゴリの取得開始")

    all_articles: list[Article] = []
    seen_urls: set[str] = set()

    for feed_config in feeds:
        articles = fetch_feed(feed_config)

        # URL重複排除
        for article in articles:
            if article["url"] not in seen_urls:
                seen_urls.add(article["url"])
                all_articles.append(article)

    # 日付の新しい順にソート
    all_articles.sort(key=lambda x: x["date"], reverse=True)

    # 最大件数に制限
    limited_articles = all_articles[:MAX_ARTICLES_PER_CATEGORY]
    print(f"[{category}] 合計: {len(all_articles)}件 → {len(limited_articles)}件に制限")

    return limited_articles


def cleanup_old_files(data_dir: Path, keep_days: int) -> None:
    """
    古いJSONファイルを削除

    Args:
        data_dir: データディレクトリ
        keep_days: 保持する日数
    """
    if not data_dir.exists():
        return

    cutoff_date = datetime.now(JST).date() - timedelta(days=keep_days)
    deleted_count = 0

    for json_file in data_dir.glob("*.json"):
        try:
            # ファイル名から日付を抽出（YYYY-MM-DD.json）
            file_date_str = json_file.stem
            file_date = datetime.strptime(file_date_str, "%Y-%m-%d").date()

            if file_date < cutoff_date:
                json_file.unlink()
                deleted_count += 1
                print(f"  削除: {json_file.name}")
        except (ValueError, OSError) as e:
            # 日付形式でないファイルや削除エラーはスキップ
            print(f"  スキップ: {json_file.name} - {e}")

    if deleted_count > 0:
        print(f"古いファイルを{deleted_count}件削除しました")


def save_news_data(data: NewsData, data_dir: Path) -> Path:
    """
    ニュースデータをJSONファイルに保存

    Args:
        data: ニュースデータ
        data_dir: 保存先ディレクトリ

    Returns:
        保存したファイルのパス
    """
    # ディレクトリが存在しない場合は作成
    data_dir.mkdir(parents=True, exist_ok=True)

    file_path = data_dir / f"{data['date']}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return file_path


def main() -> None:
    """メイン処理"""
    print("=" * 60)
    print("RSSニュース取得スクリプト")
    print("=" * 60)

    now = datetime.now(JST)
    today_str = now.strftime("%Y-%m-%d")
    updated_at = now.isoformat()

    print(f"実行日時: {updated_at}")
    print(f"データ保存先: {DATA_DIR}")

    # 各カテゴリのニュースを取得
    consulting_news = fetch_category_news("consulting", RSS_FEEDS["consulting"])
    ai_news = fetch_category_news("ai", RSS_FEEDS["ai"])
    poker_news = fetch_category_news("poker", RSS_FEEDS["poker"])

    # ニュースデータを構築
    news_data: NewsData = {
        "date": today_str,
        "updated_at": updated_at,
        "consulting": consulting_news,
        "ai": ai_news,
        "poker": poker_news,
    }

    # JSONファイルに保存
    print("\n" + "-" * 40)
    saved_path = save_news_data(news_data, DATA_DIR)
    print(f"保存完了: {saved_path}")

    # 古いファイルをクリーンアップ
    print("\n古いファイルのクリーンアップ:")
    cleanup_old_files(DATA_DIR, KEEP_DAYS)

    # サマリー表示
    print("\n" + "=" * 60)
    print("取得結果サマリー")
    print("=" * 60)
    print(f"  コンサル業界: {len(consulting_news)}件")
    print(f"  AI: {len(ai_news)}件")
    print(f"  ポーカー: {len(poker_news)}件")
    print(f"  合計: {len(consulting_news) + len(ai_news) + len(poker_news)}件")
    print("=" * 60)


if __name__ == "__main__":
    main()

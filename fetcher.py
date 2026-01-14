import feedparser
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

# --- CONFIGURATION ---
RSS_FEEDS = {
    'TechCrunch': 'https://techcrunch.com/feed/',
    'Hacker News': 'https://hnrss.org/frontpage',
    'Ars Technica': 'https://feeds.arstechnica.com/arstechnica/index',
    'GitHub Trending': 'https://mshibanami.github.io/GitHubTrendingRSS/daily/all.xml',
    'The Hacker News': 'https://feeds.feedburner.com/TheHackersNews',
}

TLDR_CATS = ['tech', 'ai']

def get_db_conn():
    return sqlite3.connect('news.db')

def save_articles(articles):
    conn = get_db_conn()
    cursor = conn.cursor()
    for art in articles:
        cursor.execute('''
            INSERT OR IGNORE INTO articles (link, title, source, summary)
            VALUES (?, ?, ?, ?)
        ''', (art['link'], art['title'], art['source'], art['summary']))
    conn.commit()
    conn.close()

def fetch_rss():
    print("🚀 Fetching RSS Feeds...")
    results = []
    for name, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            results.append({
                'title': entry.get('title', ''),
                'link': entry.get('link', ''),
                'source': name,
                'summary': entry.get('summary', '')[:500]
            })
    return results

def fetch_tldr_today():
    """Scrapes today's TLDR issues with a retry loop if not yet published."""
    today_str = datetime.now().strftime('%Y-%m-%d')
    results = []
    
    for cat in TLDR_CATS:
        url = f"https://tldr.tech/{cat}/{today_str}"
        print(f"📡 Hunting for TLDR {cat.upper()} at {url}...")
        
        # Retry loop: Tries 5 times every 2 mins if page is 404
        success = False
        for attempt in range(5):
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                # Targeted 2026 selector: find all story blocks
                # TLDR usually wraps stories in divs with specific classes or nearby <a> tags
                items = soup.find_all(['div', 'article'])
                for item in items:
                    link_tag = item.find('a', href=True)
                    if link_tag and 'tldr.tech' not in link_tag['href'] and len(link_tag.text) > 10:
                        results.append({
                            'title': link_tag.get_text(strip=True),
                            'link': link_tag['href'],
                            'source': f'TLDR_{cat.upper()}',
                            'summary': item.get_text(" ", strip=True)[:300]
                        })
                print(f"✅ Captured {cat.upper()} issue.")
                success = True
                break
            elif res.status_code == 404:
                print(f"⏳ {cat.upper()} not live yet. Retrying in 2 mins...")
                time.sleep(120)
            else:
                break
        if not success:
            print(f"❌ Failed to find TLDR {cat.upper()} for today.")
            
    return results

if __name__ == "__main__":
    # 1. RSS Pass
    rss_items = fetch_rss()
    save_articles(rss_items)
    
    # 2. TLDR Pass (Today Only)
    tldr_items = fetch_tldr_today()
    save_articles(tldr_items)
    
    print(f"✨ Sync Complete. Check DBeaver for new 'is_read=0' entries!")
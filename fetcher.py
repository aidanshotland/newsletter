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
    return sqlite3.connect('articles.db')

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
    today = datetime.now().date()
    
    for name, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        
        # GitHub Trending is a special case - it's already filtered to "today" by the feed itself
        if 'github' in name.lower() and 'trending' in name.lower():
            for entry in feed.entries:
                results.append({
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'source': name,
                    'summary': entry.get('summary', '')[:500]
                })
        else:
            # For regular RSS feeds, filter by publish date
            for entry in feed.entries:
                pub_date = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6]).date()
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    pub_date = datetime(*entry.updated_parsed[:6]).date()
                
                # Only include if published today
                if pub_date == today:
                    results.append({
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'source': name,
                        'summary': entry.get('summary', '')[:500]
                    })
    
    print(f"✅ Found {len(results)} articles from today across all RSS feeds.")
    return results

def fetch_tldr_today():
    """Scrapes today's TLDR issues with a retry loop if not yet published."""
    today_str = datetime.now().strftime('%Y-%m-%d')
    results = []
    
    for cat in TLDR_CATS:
        url = f"https://tldr.tech/{cat}/{today_str}"
        print(f"📡 Hunting for TLDR {cat.upper()} at {url}...")
        
        success = False
        for attempt in range(5):
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                
                # Find all story blocks (divs or articles)
                items = soup.find_all(['div', 'article'])
                seen_links = set()  # Avoid duplicates
                
                for item in items:
                    # Find ALL links in this item
                    links_in_item = item.find_all('a', href=True)
                    
                    # Find the BEST link (longest title text, external, not seen)
                    best_link = None
                    best_title = ""
                    
                    for link_tag in links_in_item:
                        href = link_tag['href']
                        title = link_tag.get_text(strip=True)
                        
                        # Must be external and not already captured
                        if (href.startswith('http') and 
                            'tldr.tech' not in href and 
                            'unsubscribe' not in href.lower() and
                            href not in seen_links and
                            len(title) > len(best_title) and
                            len(title) > 10):
                            
                            best_link = href
                            best_title = title
                    
                    # If we found a good link, save it
                    if best_link:
                        seen_links.add(best_link)
                        results.append({
                            'title': best_title,
                            'link': best_link,
                            'source': f'TLDR_{cat.upper()}',
                            'summary': item.get_text(" ", strip=True)[:300]
                        })
                
                print(f"✅ Captured {len([r for r in results if r['source'] == f'TLDR_{cat.upper()}'])} articles from {cat.upper()} issue.")
                success = True
                break
            elif res.status_code == 404:
                print(f"⏳ {cat.upper()} not live yet. Retrying in 2 mins...")
                time.sleep(120)
            else:
                print(f"❌ Unexpected status {res.status_code} for {cat.upper()}")
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
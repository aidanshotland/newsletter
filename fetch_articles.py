import feedparser
from datetime import datetime, timedelta

# RSS feeds for your tech sources
FEEDS = {
    'TechCrunch': 'https://techcrunch.com/feed/',
    'Hacker News': 'https://hnrss.org/frontpage',
    'The Verge': 'https://www.theverge.com/rss/index.xml',
    'Ars Technica': 'https://feeds.arstechnica.com/arstechnica/index',
    'arXiv CS': 'https://rss.arxiv.org/rss/cs',
    'GitHub Trending': 'https://mshibanami.github.io/GitHubTrendingRSS/daily/all.xml',
    'AWS Security': 'https://aws.amazon.com/blogs/security/feed/',
    'TechCrunch AI': 'https://techcrunch.com/category/artificial-intelligence/feed/',
    'The Hacker News': 'https://feeds.feedburner.com/TheHackersNews',
}

def fetch_recent_articles(hours=24):
    """Fetch articles from the last N hours from all feeds."""
    all_articles = []
    cutoff_time = datetime.now() - timedelta(hours=hours)
    
    # Sources that don't have per-article dates (already filtered by the feed itself)
    NO_DATE_SOURCES = ['GitHub Trending']
    
    for source_name, feed_url in FEEDS.items():
        print(f"\nFetching from {source_name}...")
        
        try:
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries[:10]:  # Limit to 10 most recent per source
                # Parse publication date
                pub_date = None
                if hasattr(entry, 'published_parsed'):
                    pub_date = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed'):
                    pub_date = datetime(*entry.updated_parsed[:6])
                
                # Get full summary/description from RSS feed
                summary = entry.get('summary', entry.get('description', 'No summary available'))
                
                # For sources without dates, include all items (they're pre-filtered)
                if source_name in NO_DATE_SOURCES:
                    article = {
                        'source': source_name,
                        'title': entry.title,
                        'link': entry.link,
                        'published': 'Recent',
                        'summary': summary
                    }
                    all_articles.append(article)
                # For other sources, only include recent articles
                elif pub_date and pub_date > cutoff_time:
                    article = {
                        'source': source_name,
                        'title': entry.title,
                        'link': entry.link,
                        'published': pub_date.strftime('%Y-%m-%d %H:%M'),
                        'summary': summary
                    }
                    all_articles.append(article)
                    
            print(f"Found {len([a for a in all_articles if a['source'] == source_name])} recent articles")
            
        except Exception as e:
            print(f"Error fetching {source_name}: {e}")
    
    return all_articles

if __name__ == "__main__":
    print("Fetching articles from the last 24 hours...\n")
    articles = fetch_recent_articles(hours=24)
    
    print(f"\n{'='*80}")
    print(f"Total articles found: {len(articles)}")
    print(f"{'='*80}\n")
    
    # Display the articles
    for i, article in enumerate(articles, 1):
        print(f"{i}. [{article['source']}] {article['title']}")
        print(f"   Published: {article['published']}")
        print(f"   Link: {article['link']}")
        print(f"   Summary: {article['summary'][:300]}..." if len(article['summary']) > 300 else f"   Summary: {article['summary']}")
        print()
import feedparser
from datetime import datetime, timedelta

# RSS feeds for your tech sources
RSS_FEEDS = {
    'TechCrunch': 'https://techcrunch.com/feed/',
    'Hacker News': 'https://hnrss.org/frontpage',
    'Ars Technica': 'https://feeds.arstechnica.com/arstechnica/index',
    'arXiv CS': 'https://rss.arxiv.org/rss/cs',
    'GitHub Trending': 'https://mshibanami.github.io/GitHubTrendingRSS/daily/all.xml',
    'AWS Security': 'https://aws.amazon.com/blogs/security/feed/',
    'The Hacker News': 'https://feeds.feedburner.com/TheHackersNews',
}

# Newsletter sources (to be ingested from email)
NEWSLETTERS = {
    'TLDR': {'source': 'email_ingest'},
    'TLDR AI': {'source': 'email_ingest'},
}

def parse_newsletter_file(filename='newsletters.txt'):
    """Parse newsletter file. Format: title line, description (1+ lines), blank line."""
    articles = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by double newlines to get article blocks
        blocks = content.strip().split('\n\n')
        
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 2:
                title = lines[0].strip()
                # Join all remaining lines as the description
                description = ' '.join(line.strip() for line in lines[1:])
                
                if title and description:
                    article = {
                        'source': 'Newsletter',
                        'title': title,
                        'link': '',
                        'published': datetime.now().strftime('%Y-%m-%d %H:%M'),
                        'summary': description
                    }
                    articles.append(article)
        
        print(f"\nParsed {len(articles)} articles from {filename}")
        
    except FileNotFoundError:
        print(f"\nNo {filename} file found - skipping newsletter articles")
    except Exception as e:
        print(f"\nError reading {filename}: {e}")
    
    return articles

def fetch_recent_articles(hours=24):
    """Fetch articles from the last N hours from all feeds."""
    all_articles = []
    cutoff_time = datetime.now() - timedelta(hours=hours)
    
    # Sources that don't have per-article dates (already filtered by the feed itself)
    NO_DATE_SOURCES = ['GitHub Trending']
    
    for source_name, feed_url in RSS_FEEDS.items():
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
                
                # For sources without dates, include all items (they're pre-filtered)
                if source_name in NO_DATE_SOURCES:
                    article = {
                        'source': source_name,
                        'title': entry.title,
                        'link': entry.link,
                        'published': 'Recent',
                        'summary': entry.get('summary', '')
                    }
                    all_articles.append(article)
                # For other sources, only include recent articles
                elif pub_date and pub_date > cutoff_time:
                    article = {
                        'source': source_name,
                        'title': entry.title,
                        'link': entry.link,
                        'published': pub_date.strftime('%Y-%m-%d %H:%M'),
                        'summary': entry.get('summary', '')
                    }
                    all_articles.append(article)
                    
            print(f"Found {len([a for a in all_articles if a['source'] == source_name])} recent articles")
            
        except Exception as e:
            print(f"Error fetching {source_name}: {e}")
    
    # Add newsletter articles from manual file
    newsletter_articles = parse_newsletter_file()
    all_articles.extend(newsletter_articles)
    
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
        print(f"   Preview: {article['summary']}")
        print()
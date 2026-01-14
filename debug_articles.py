import feedparser
from datetime import datetime, timedelta

feed = feedparser.parse('https://krebsonsecurity.com/feed/')
cutoff = datetime.now() - timedelta(hours=24)

print('Feed has', len(feed.entries), 'total entries')
print('Current time:', datetime.now())
print('Cutoff time (24h ago):', cutoff)
print()

for entry in feed.entries[:3]:
    print('Title:', entry.title[:50])
    print('Has published_parsed:', hasattr(entry, 'published_parsed'))
    if hasattr(entry, 'published_parsed'):
        pub_date = datetime(*entry.published_parsed[:6])
        print('Published:', pub_date)
        print('After cutoff?', pub_date > cutoff)
    print()

import feedparser

def fetch_korean_news():
    url = "https://news.google.com/rss/search?q=한국경제&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(url)
    return [item.title for item in feed.entries[:5]]

def fetch_us_news():
    url = "https://news.google.com/rss/search?q=stock+market+economy&hl=en&gl=US&ceid=US:en"
    feed = feedparser.parse(url)
    return [item.title for item in feed.entries[:5]]

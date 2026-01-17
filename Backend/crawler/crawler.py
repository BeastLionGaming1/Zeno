from config import SEED_URLS, MAX_PAGES, CRAWL_DELAY, DB_FILE, ALLOWED_DOMAINS
from utils import get_links, normalize_url

import requests
from bs4 import BeautifulSoup
import sqlite3
from urllib.parse import urljoin, urlparse
import time

# ---------------------------
# CONFIGURATION
# ---------------------------
SEED_URLS = [
    "https://google.com",  # Replace with sites you want to crawl
]
MAX_PAGES = 50  # Limit number of pages to crawl
CRAWL_DELAY = 1  # Seconds between requests to be polite

DB_FILE = "db/pages.sqlite"

# ---------------------------
# DATABASE SETUP
# ---------------------------
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE,
    html TEXT
)
''')
conn.commit()

# ---------------------------
# CRAWLER LOGIC
# ---------------------------
visited = set()
queue = SEED_URLS.copy()

def get_links(url, html):
    """Extract all internal links from a page."""
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for a_tag in soup.find_all("a", href=True):
        href = a_tag['href']
        # Make absolute URL
        full_url = urljoin(url, href)
        # Only crawl same domain
        if urlparse(full_url).netloc == urlparse(url).netloc:
            links.add(full_url)
    return links

def crawl():
    pages_crawled = 0

    while queue and pages_crawled < MAX_PAGES:
        url = queue.pop(0)
        if url in visited:
            continue

        try:
            print(f"Crawling: {url}")
            response = requests.get(url, timeout=5)
            html = response.text

            # Save to database
            cursor.execute("INSERT OR IGNORE INTO pages (url, html) VALUES (?, ?)", (url, html))
            conn.commit()

            visited.add(url)
            pages_crawled += 1

            # Extract links and add to queue
            links = get_links(url, html)
            for link in links:
                if link not in visited:
                    queue.append(link)

            time.sleep(CRAWL_DELAY)  # Be polite

        except Exception as e:
            print(f"Failed to crawl {url}: {e}")

    print(f"Crawling complete. {pages_crawled} pages saved.")

if __name__ == "__main__":
    crawl()
    conn.close()
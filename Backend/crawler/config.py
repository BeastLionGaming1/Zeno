# ---------------------------
# CRAWLER CONFIGURATION
# ---------------------------

# Seed URLs to start crawling from
SEED_URLS = [
    "https://google.com",  # Replace with the site(s) you want to crawl
]

# Maximum number of pages to crawl
MAX_PAGES = 50

# Seconds to wait between requests to avoid overloading servers
CRAWL_DELAY = 1

# SQLite database file path
DB_FILE = "db/pages.sqlite"

# Optional: restrict crawler to only certain domains
# Leave empty to allow any domain
ALLOWED_DOMAINS = []  # e.g., ["google.com"]
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

def get_links(base_url, html, allowed_domains=None):
    """
    Extract all valid links from a page HTML.

    - base_url: current page URL to resolve relative links
    - html: HTML content of the page
    - allowed_domains: list of domains to restrict crawling (optional)
    """
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for a_tag in soup.find_all("a", href=True):
        href = a_tag['href']
        full_url = urljoin(base_url, href)  # Convert relative URLs to absolute
        domain = urlparse(full_url).netloc

        # Skip if allowed_domains is set and domain not in it
        if allowed_domains and domain not in allowed_domains:
            continue

        links.add(full_url)

    return links


def normalize_url(url):
    """
    Clean up URLs by removing fragments and query parameters if desired.
    """
    parsed = urlparse(url)
    # Reconstruct URL without fragment
    normalized = parsed.scheme + "://" + parsed.netloc + parsed.path
    return normalized.rstrip("/")
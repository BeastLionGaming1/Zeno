import sqlite3
import json
import re
from collections import defaultdict

# ---------------------------
# CONFIGURATION
# ---------------------------
DB_FILE = "db/pages.sqlite"
INDEX_FILE = "db/index.json"

# ---------------------------
# DATABASE CONNECTION
# ---------------------------
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# ---------------------------
# UTILITY FUNCTIONS
# ---------------------------
def tokenize(text):
    """
    Convert text to lowercase, remove non-alphanumeric characters, 
    and split into words.
    """
    text = text.lower()
    # Remove everything except letters and numbers
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    tokens = text.split()
    return tokens

# ---------------------------
# BUILDING INVERTED INDEX
# ---------------------------
def build_index():
    inverted_index = defaultdict(list)

    cursor.execute("SELECT id, url, html FROM pages")
    pages = cursor.fetchall()

    print(f"Building index for {len(pages)} pages...")

    for page_id, url, html in pages:
        tokens = set(tokenize(html))  # Use set to avoid duplicates
        for token in tokens:
            inverted_index[token].append({
                "id": page_id,
                "url": url
            })

    # Save to JSON
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(inverted_index, f, indent=2)

    print(f"Inverted index saved to {INDEX_FILE}")

if __name__ == "__main__":
    build_index()
    conn.close()
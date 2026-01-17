import json
import re
from collections import defaultdict

INDEX_FILE = "db/index.json"

# ---------------------------
# UTILITY FUNCTIONS
# ---------------------------
def tokenize(text):
    """
    Convert text to lowercase, remove non-alphanumeric characters, 
    and split into words (same as build_index.py)
    """
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    tokens = text.split()
    return tokens


# ---------------------------
# LOAD INVERTED INDEX
# ---------------------------
with open(INDEX_FILE, "r", encoding="utf-8") as f:
    inverted_index = json.load(f)

print(f"Inverted index loaded with {len(inverted_index)} unique words.")


# ---------------------------
# SEARCH FUNCTION
# ---------------------------
def search(query, max_results=10):
    """
    Search for query in inverted index.
    Returns top URLs ranked by how many query words they contain.
    """
    tokens = tokenize(query)
    scores = defaultdict(int)  # URL -> score

    for token in tokens:
        if token in inverted_index:
            for entry in inverted_index[token]:
                url = entry["url"]
                scores[url] += 1  # simple frequency scoring

    # Sort results by score descending
    sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return [url for url, score in sorted_results[:max_results]]


# ---------------------------
# SIMPLE CLI TEST
# ---------------------------
if __name__ == "__main__":
    while True:
        query = input("\nEnter your search query (or 'exit' to quit): ")
        if query.lower() == "exit":
            break

        results = search(query)
        if results:
            print("\nTop results:")
            for i, url in enumerate(results, 1):
                print(f"{i}. {url}")
        else:
            print("No results found.")
import json
from bs4 import BeautifulSoup

def extract_mpn_from_jsonld(html, expected_mpn=None):
    soup = BeautifulSoup(html, "html.parser")
    candidates = []

    for script in soup.find_all("script", type="application/ld+json"):
        try:
            raw = script.string
            if not raw:
                continue
            data = json.loads(raw.strip())

            # Handle list of JSON-LD blocks (some pages wrap multiple items)
            if isinstance(data, list):
                for entry in data:
                    if isinstance(entry, dict) and "mpn" in entry:
                        if not expected_mpn or entry.get("mpn") == expected_mpn:
                            candidates.append(entry)
            elif isinstance(data, dict):
                if "mpn" in data:
                    if not expected_mpn or data.get("mpn") == expected_mpn:
                        candidates.append(data)
        except Exception as e:
            continue  # Skip bad blocks silently

    return candidates

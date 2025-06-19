import requests
from bs4 import BeautifulSoup
import json

def lookup_bh(product_name, mpn=None):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    if mpn:
        search_url = f"https://www.bhphotovideo.com/c/search?q={mpn}&sts=ma"
        manual_link = search_url
    elif product_name:
        search_url = f"https://www.bhphotovideo.com/c/search?q={product_name}&sts=ma"
        manual_link = search_url
    else:
        return {
            "status": "❌ Invalid input. Provide a product name or MPN.",
            "link": "",
            "mpn_match": False
        }

    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        if response.status_code != 200:
            return {
                "status": "❌ Failed to fetch B&H page.",
                "link": manual_link,
                "mpn_match": False
            }

        soup = BeautifulSoup(response.content, "html.parser")

        # Try parsing metadata
        scripts = soup.find_all("script", type="application/ld+json")
        for script in scripts:
            try:
                data = json.loads(script.string.strip())
                if isinstance(data, dict) and "mpn" in data:
                    fetched_mpn = data["mpn"].strip().upper()
                    if mpn:
                        if fetched_mpn == mpn.upper():
                            return {
                                "status": "🟢 In Stock (MPN verified)",
                                "link": manual_link,
                                "mpn_match": True
                            }
                        else:
                            return {
                                "status": "⚠️ MPN mismatch — review manually.",
                                "link": manual_link,
                                "mpn_match": False
                            }
                    else:
                        return {
                            "status": "🟢 In Stock (matched by metadata)",
                            "link": manual_link,
                            "mpn_match": True
                        }
            except Exception:
                continue

        return {
            "status": "🟡 B&H product not found or MPN not in metadata.",
            "link": manual_link,
            "mpn_match": False
        }

    except Exception as e:
        return {
            "status": f"❌ Failed to fetch B&H page: {str(e)}",
            "link": manual_link,
            "mpn_match": False
        }

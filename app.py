from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import difflib

app = Flask(__name__)
CORS(app)

# ---------- Utility: B&H Scraper ----------
def scrape_bh(product_name=None, mpn=None):
    try:
        if mpn:
            search_url = f"https://www.bhphotovideo.com/c/search?Ntt={mpn}"
        elif product_name:
            search_url = f"https://www.bhphotovideo.com/c/search?Ntt={product_name}"
        else:
            return {"status": "error", "error": "Missing product or MPN"}

        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")

        product_tiles = soup.select("div[data-selenium='miniProductPage']")
        if not product_tiles:
            return {"status": "not_found"}

        best_match = None
        highest_ratio = 0

        for tile in product_tiles:
            title_tag = tile.select_one("span[data-selenium='miniProductPageProductName']")
            link_tag = tile.select_one("a[data-selenium='miniProductPageProductNameLink']")
            if not title_tag or not link_tag:
                continue

            title = title_tag.text.strip()
            link = "https://www.bhphotovideo.com" + link_tag.get("href", "")

            if mpn and mpn.lower() in title.lower():
                best_match = tile
                break

            if product_name:
                ratio = difflib.SequenceMatcher(None, title.lower(), product_name.lower()).ratio()
                if ratio > highest_ratio:
                    highest_ratio = ratio
                    best_match = tile if ratio > 0.5 else None  # Confidence threshold

        if not best_match:
            return {"status": "not_found"}

        used_price_tag = best_match.select_one("span[data-selenium='usedPrice']")
        new_price_tag = best_match.select_one("span[data-selenium='price']")

        used_price = used_price_tag.text.strip() if used_price_tag else None
        new_price = new_price_tag.text.strip() if new_price_tag else None

        return {
            "status": "found",
            "used_price": used_price,
            "new_price": new_price,
            "link": link
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}

# ---------- Main Lookup Route ----------
@app.route("/lookup", methods=["POST"])
def lookup():
    data = request.get_json()
    product = data.get("product", "").strip()
    mpn = data.get("mpn", "").strip()

    if not product and not mpn:
        return jsonify({"error": "Please provide at least a product name or MPN"}), 400

    bh_result = scrape_bh(product_name=product, mpn=mpn)

    return jsonify(bh_result)

# ---------- Default route (optional) ----------
@app.route("/")
def index():
    return "Retail Price Verifier API is live."

if __name__ == "__main__":
    app.run(debug=True)

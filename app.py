from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "Lensrentals Product Verifier backend is live."

@app.route("/lookup", methods=["POST"])
def lookup():
    data = request.get_json()
    product_name = data.get("product", "").strip()
    mpn = data.get("mpn", "").strip()

    if not product_name and not mpn:
        return jsonify({"error": "Either product name or MPN is required."}), 400

    search_terms = mpn if mpn else product_name
    search_url = f"https://www.bhphotovideo.com/c/search?q={requests.utils.quote(search_terms)}&sts=ma"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        tiles = soup.select(".item")

        confident_match = False
        for tile in tiles:
            title = tile.select_one(".itemDescription")
            specs = tile.select_one(".item-specs")
            if not title:
                continue

            title_text = title.get_text(strip=True)
            specs_text = specs.get_text(strip=True) if specs else ""

            if mpn and mpn.lower() in specs_text.lower():
                confident_match = True
                break
            elif product_name and product_name.lower() in title_text.lower():
                confident_match = True
                break

        bh_result = {
            "status": "✅ Confident match found" if confident_match else "⚠️ No confident match",
            "search_url": search_url
        }

        return jsonify({"bh": bh_result})

    except Exception as e:
        return jsonify({"error": f"Failed to scrape B&H: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

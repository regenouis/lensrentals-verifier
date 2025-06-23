from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Lensrentals Product Verifier backend is live."

@app.route("/lookup", methods=["POST"])
def lookup():
    data = request.get_json(force=True)

    product_name = data.get("product", "").strip()
    mpn = data.get("mpn", "").strip()

    bh_result = get_bh_data(product_name, mpn)

    return jsonify({"bh": bh_result})

def get_bh_data(product_name, mpn):
    search_url = f"https://www.bhphotovideo.com/c/search?Ntt={mpn}&N=0&InitialSearch=yes&sts=ma"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Look for matching product tiles
        tiles = soup.select(".item-details")
        for tile in tiles:
            title = tile.get_text(strip=True).lower()
            if mpn.lower() in title or product_name.lower() in title:
                return {
                    "status": "Confident match found",
                    "search_url": search_url
                }

        return {
            "status": "No confident match",
            "search_url": search_url
        }

    except Exception as e:
        return {
            "status": f"Error: {str(e)}",
            "search_url": search_url
        }

if __name__ == "__main__":
    app.run(debug=True)

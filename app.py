from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Lensrentals Verifier Backend is live."

@app.route("/lookup_bh", methods=["POST"])
def lookup_bh():
    data = request.json
    product_name = data.get("product_name")
    mpn = data.get("mpn")

    headers = {"User-Agent": "Mozilla/5.0"}
    query = mpn or product_name
    search_url = f"https://www.bhphotovideo.com/c/search?q={query}&sts=ma"

    result = {
        "bh": {
            "link": search_url,
            "status": "",
            "mpn_match": False,
            "error": False,
            "review_flag": False
        }
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        if response.status_code != 200:
            result["bh"]["status"] = f"⚠️ Manual review required — B&H returned {response.status_code}"
            result["bh"]["error"] = True
            result["bh"]["review_flag"] = True
            return jsonify(result)

        soup = BeautifulSoup(response.content, "html.parser")
        scripts = soup.find_all("script", type="application/ld+json")

        for script in scripts:
            if not script.string:
                continue
            try:
                data = json.loads(script.string.strip())
                if isinstance(data, dict) and "mpn" in data:
                    found_mpn = data["mpn"].strip().upper()
                    if mpn and found_mpn == mpn.upper():
                        result["bh"]["status"] = "🟢 In Stock (MPN verified)"
                        result["bh"]["mpn_match"] = True
                        return jsonify(result)
                    elif mpn:
                        result["bh"]["status"] = f"⚠️ MPN mismatch — found `{found_mpn}`"
                        result["bh"]["review_flag"] = True
                        return jsonify(result)
                    else:
                        result["bh"]["status"] = "🟢 In Stock (metadata present)"
                        result["bh"]["mpn_match"] = True
                        return jsonify(result)
            except json.JSONDecodeError:
                continue

        result["bh"]["status"] = "🟡 Metadata not found — manual review suggested"
        result["bh"]["review_flag"] = True
        return jsonify(result)

    except Exception as e:
        result["bh"]["status"] = f"❌ Fetch error: {str(e)}"
        result["bh"]["error"] = True
        result["bh"]["review_flag"] = True
        return jsonify(result)

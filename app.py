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
    if not query:
        return jsonify({"status": "❌ No input provided."}), 400

    search_url = f"https://www.bhphotovideo.com/c/search?q={query}&sts=ma"
    result = {
        "link": search_url,
        "status": "",
        "mpn_match": False,
        "error": False
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        if response.status_code != 200:
            result["status"] = f"❌ Failed to fetch B&H page (status {response.status_code})"
            result["error"] = True
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
                        result["status"] = "🟢 In Stock (MPN verified)"
                        result["mpn_match"] = True
                        return jsonify(result)
                    elif mpn:
                        result["status"] = f"⚠️ MPN mismatch — found `{found_mpn}`"
                        return jsonify(result)
                    else:
                        result["status"] = "🟢 In Stock (metadata present)"
                        result["mpn_match"] = True
                        return jsonify(result)
            except json.JSONDecodeError:
                continue

        result["status"] = "🟡 Metadata not found — review manually."
        return jsonify(result)

    except Exception as e:
        result["status"] = f"❌ Fetch error: {str(e)}"
        result["error"] = True
        return jsonify(result)

from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route("/")
def retail_price_viewer():
    return render_template("retail_price_viewer.html")

@app.route("/lookup_bh", methods=["POST"])
def lookup_bh():
    data = request.get_json()
    product_name = data.get("product_name")
    mpn = data.get("mpn")
    
    bh_url = f"https://www.bhphotovideo.com/c/search?q={mpn}&sts=ma"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        res = requests.get(bh_url, headers=headers, timeout=10)
        if res.status_code != 200:
            return jsonify({"error": True, "link": bh_url, "mpn_match": False, "status": f"Failed to fetch B&H page (status {res.status_code})"})
        soup = BeautifulSoup(res.text, "html.parser")
        product_blocks = soup.find_all("div", class_="itemWrapper")
        match_found = False
        for block in product_blocks:
            if mpn.lower() in block.text.lower():
                match_found = True
                break
        return jsonify({
            "error": False,
            "link": bh_url,
            "mpn_match": match_found,
            "status": "MPN match found" if match_found else "MPN not found"
        })
    except Exception as e:
        return jsonify({"error": True, "link": bh_url, "mpn_match": False, "status": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)

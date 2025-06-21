from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("retail_price_viewer.html")

@app.route("/lookup", methods=["POST"])
def lookup():
    product_name = request.form.get("product_name", "").strip()
    mpn = request.form.get("mpn", "").strip()

    if not product_name and not mpn:
        return render_template("retail_price_viewer.html", results=None, error="Please enter a product name.")

    # Example mocked results; replace this with your actual price checking logic
    results = {
        "B&H": {
            "status": "Found" if mpn else "Manual Review",
            "price": "$1999.00" if mpn else "N/A",
            "url": f"https://www.bhphotovideo.com/c/search?q={mpn or product_name}"
        },
        "Adorama": {
            "status": "Found" if mpn else "Not Found",
            "price": "$1979.00" if mpn else "N/A",
            "url": f"https://www.adorama.com/l/?searchinfo={mpn or product_name}"
        },
        "eBay": {
            "status": "Check Manually",
            "price": "See sold listings",
            "url": f"https://www.ebay.com/sch/i.html?_nkw={mpn or product_name}"
        },
        "MPB": {
            "status": "Available",
            "price": "$1899.00",
            "url": f"https://www.mpb.com/en-us/search/?q={mpn or product_name}"
        }
    }

    return render_template("retail_price_viewer.html", results=results, error=None)

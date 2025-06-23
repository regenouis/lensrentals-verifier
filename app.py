from flask import Flask, render_template, request
from urllib.parse import quote_plus

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('retail_price_viewer.html')

@app.route('/lookup', methods=['POST'])
def lookup():
    product_name = request.form.get('product_name', '').strip()
    mpn = request.form.get('mpn', '').strip()

    # Prioritize MPN if provided, else fallback to product name
    query = quote_plus(mpn if mpn else product_name)
    bh_url = f"https://www.bhphotovideo.com/c/search?Ntt={query}&N=0&InitialSearch=yes"

    # Example result structure
    results = {
        "B&H": {
            "status": "Found",
            "new_price": "$2,495",
            "used_price": "$2,199",
            "link": bh_url
        },
        "eBay": {
            "status": "No results",
            "new_price": None,
            "used_price": None,
            "link": None
        }
    }

    return render_template('retail_price_viewer.html', results=results)

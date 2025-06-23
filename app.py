from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('retail_price_viewer.html')

@app.route('/lookup', methods=['POST'])
def lookup():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No JSON payload received'}), 400

    product_name = data.get('product_name', '').strip()
    mpn = data.get('mpn', '').strip()

    if not product_name and not mpn:
        return jsonify({'error': 'Please provide either a product name or MPN'}), 400

    # For now, simulate scraper output with dummy data
    # In real implementation, this will use requests/BeautifulSoup to fetch & parse real pages
    bh_result = {
        'price': 'In Stock — $3,199.99',
        'url': f"https://www.bhphotovideo.com/c/search?Ntt={mpn or product_name}&N=0"
    }

    adorama = 'Out of Stock'
    ebay_sold = '$2,950 avg (last 3 sold)'
    mpb = 'Used — $2,780'

    results = {
        'product_name': product_name,
        'mpn': mpn,
        'bh_photo': f"<a href='{bh_result['url']}' target='_blank'>{bh_result['price']}</a>",
        'adorama': f"<a href='https://www.adorama.com' target='_blank'>{adorama}</a>",
        'ebay_sold': f"<a href='https://www.ebay.com/sch/i.html?_nkw={mpn or product_name}&LH_Sold=1' target='_blank'>{ebay_sold}</a>",
        'mpb': f"<a href='https://www.mpb.com/en-us/' target='_blank'>{mpb}</a>"
    }

    return jsonify(results)

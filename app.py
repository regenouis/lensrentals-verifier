from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

def fetch_bh_data(mpn):
    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = f"https://www.bhphotovideo.com/c/search?Ntt={mpn}&N=0&InitialSearch=yes&sts=ma"
    search_resp = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(search_resp.text, 'html.parser')

    result_cards = soup.select('.resultItem')
    for card in result_cards:
        mpn_tag = card.select_one('[data-selenium="manufacturerProductNumber"]')
        if mpn_tag and mpn.lower() in mpn_tag.text.strip().lower():
            link_tag = card.select_one('a[href*="/c/product/"]')
            if link_tag:
                product_url = f"https://www.bhphotovideo.com{link_tag['href']}"
                product_resp = requests.get(product_url, headers=headers)
                product_soup = BeautifulSoup(product_resp.text, 'html.parser')

                title_tag = product_soup.select_one('h1')
                price_tag = product_soup.select_one('span[itemprop="price"]')
                used_price_tag = product_soup.find('a', string=lambda text: text and "Used" in text)

                return {
                    "status": "In Stock" if price_tag else "Out of Stock",
                    "price": f"${price_tag.text.strip()}" if price_tag else "N/A",
                    "used_price": used_price_tag.text.strip() if used_price_tag else None,
                    "link": product_url,
                    "warning": None
                }

    return {
        "status": "No match found",
        "price": None,
        "used_price": None,
        "link": search_url,
        "warning": "Could not verify MPN match"
    }

@app.route('/')
def index():
    return render_template('retail_price_viewer.html')

@app.route('/check_prices', methods=['POST'])
def check_prices():
    data = request.json
    name = data.get('name', '').strip()
    mpn = data.get('mpn', '').strip()

    if not name and not mpn:
        return jsonify({'error': 'Please enter a product name or MPN'}), 400

    results = {
        'bh': fetch_bh_data(mpn) if mpn else {"status": "No MPN provided", "price": None},
        'adorama': {'status': 'Out of Stock'},
        'ebay': {'status': 'Sold', 'price': '$2,950 avg (last 3 sold)'},
        'mpb': {'status': 'Used', 'price': '$2,780'}
    }

    return jsonify(results)

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('retail_price_viewer.html')

@app.route('/lookup', methods=['POST'])
def lookup():
    data = request.form
    name = data.get('name', '').strip()
    mpn = data.get('mpn', '').strip()

    if not name and not mpn:
        return jsonify({'error': 'Please enter a product name or MPN.'}), 400

    results = {
        "bh": get_bh_price(mpn=mpn, name=name),
        "adorama": get_adorama_status(name),
        "ebay": get_ebay_price(name),
        "mpb": get_mpb_price(name)
    }

    return jsonify(results)

def get_bh_price(mpn=None, name=None):
    try:
        if mpn:
            search_url = f"https://www.bhphotovideo.com/c/search?Ntt={mpn}&N=0"
        else:
            search_url = f"https://www.bhphotovideo.com/c/search?Ntt={name}&N=0"

        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        link_tag = soup.select_one('.productList .photo a')
        if not link_tag:
            return {"status": "No match found"}

        product_url = f"https://www.bhphotovideo.com{link_tag['href']}"
        product_response = requests.get(product_url, headers=headers)
        product_soup = BeautifulSoup(product_response.text, 'html.parser')

        price_tag = product_soup.select_one('div.price_1DPoToKrLP8uWvruGqgtaY span')
        status_tag = product_soup.select_one('div.stockStatus_3u4kFCN6fFzQvcTC7uN3lJ span')
        used_price_tag = product_soup.find(string=re.compile('Used')).find_next('span') if product_soup.find(string=re.compile('Used')) else None
        matched_mpn = product_soup.find(string=re.compile('MFR #')).split('#')[-1].strip() if product_soup.find(string=re.compile('MFR #')) else None

        warning = ""
        if mpn and matched_mpn and mpn.lower() != matched_mpn.lower():
            warning = f"⚠️ MPN mismatch: matched {matched_mpn}"

        result = {
            "status": status_tag.text.strip() if status_tag else "Unknown",
            "price": price_tag.text.strip() if price_tag else "Unknown",
            "link": product_url,
            "used_price": used_price_tag.text.strip() if used_price_tag else None,
            "warning": warning
        }
        return result
    except Exception as e:
        return {"status": "Error", "error": str(e)}

def get_adorama_status(name):
    # Placeholder: replace with actual scraper or API if needed
    return {"status": "Out of Stock"}

def get_ebay_price(name):
    # Placeholder: simulate average of last 3 sold
    return {"price": "$2,950 avg (last 3 sold)"}

def get_mpb_price(name):
    # Placeholder
    return {"price": "Used — $2,780"}

if __name__ == '__main__':
    app.run(debug=True)

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

    product_name = data.get('product_name', '').strip()
    mpn = data.get('mpn', '').strip()

    if not product_name and not mpn:
        return jsonify({'error': 'Product name or MPN is required'}), 400

    bh_result = scrape_bh_by_mpn(mpn) if mpn else {'price': 'Skipped', 'url': 'https://www.bhphotovideo.com'}
    adorama = 'Out of Stock'  # Placeholder
    ebay_sold = '$2,950 avg (last 3 sold)'  # Placeholder
    mpb = 'Used — $2,780'  # Placeholder

    results = {
        'product_name': product_name,
        'mpn': mpn,
        'bh_photo': f"<a href='{bh_result['url']}' target='_blank'>{bh_result['price']}</a>",
        'adorama': f"<a href='https://www.adorama.com' target='_blank'>{adorama}</a>",
        'ebay_sold': f"<a href='https://www.ebay.com/sch/i.html?_nkw={mpn or product_name}&LH_Sold=1' target='_blank'>{ebay_sold}</a>",
        'mpb': f"<a href='https://www.mpb.com/en-us/' target='_blank'>{mpb}</a>"
    }

    return jsonify(results)


def scrape_bh_by_mpn(mpn):
    search_url = f"https://www.bhphotovideo.com/c/search?Ntt={mpn}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.select("div#gridContent div.itemWrapper_2As3T")

    if not products:
        return {'price': 'No match found', 'url': search_url}

    for product in products[:3]:
        link_tag = product.select_one("a[data-selenium='miniProductPageLink']")
        if not link_tag:
            continue
        product_url = "https://www.bhphotovideo.com" + link_tag['href']
        prod_resp = requests.get(product_url, headers=headers)
        prod_soup = BeautifulSoup(prod_resp.text, "html.parser")

        mfr_line = prod_soup.find(text=lambda t: t and "MFR #" in t)
        if mfr_line and mpn.upper() in mfr_line:
            price_tag = prod_soup.select_one(".price_1DPoToKrLP8uWvruGqgtaY")
            price = price_tag.text.strip() if price_tag else "Price not listed"
            stock_tag = prod_soup.find("div", string=lambda s: s and "In Stock" in s)
            stock_status = "In Stock" if stock_tag else "Check availability"
            return {

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

HEADERS = {'User-Agent': 'Mozilla/5.0'}

@app.route('/')
def home():
    return render_template('retail_price_viewer.html')

@app.route('/check', methods=['POST'])
def check_prices():
    data = request.get_json()
    name = data.get('name', '').strip()
    mpn = data.get('mpn', '').strip()

    if not name and not mpn:
        return jsonify({'error': 'Either name or MPN must be provided'}), 400

    results = {}

    # B&H Price
    if mpn:
        search_url = f"https://www.bhphotovideo.com/c/search?Ntt={mpn}&N=0&InitialSearch=yes&sts=ma"
        search_page = requests.get(search_url, headers=HEADERS)
        soup = BeautifulSoup(search_page.text, 'html.parser')
        product_cards = soup.find_all('div', class_='productItem')

        match_found = False
        for card in product_cards:
            product_link = card.find('a', class_='photoLink')
            if not product_link:
                continue
            product_url = f"https://www.bhphotovideo.com{product_link.get('href')}"
            product_page = requests.get(product_url, headers=HEADERS)
            product_soup = BeautifulSoup(product_page.text, 'html.parser')
            mfr_div = product_soup.find('div', class_='sku')
            if mfr_div and mpn.upper() in mfr_div.text:
                price_div = product_soup.find('div', class_='price_1DPoToKrLP8uWvruGqgtaY')
                price = price_div.text.strip() if price_div else 'Price not listed'
                used_section = product_soup.find(string="Used for")
                used_price = used_section.find_next().text.strip() if used_section else None

                results['bh'] = {
                    'status': 'In Stock',
                    'price': price,
                    'url': product_url,
                    'used_price': used_price
                }
                match_found = True
                break

        if not match_found:
            results['bh'] = {'status': 'No match found'}

    # Adorama (Placeholder only — scraping not implemented)
    results['adorama'] = {'status': 'Out of Stock'}

    # eBay sold prices (Stubbed)
    results['ebay'] = {'status': 'Sold', 'price': '$2,950 avg (last 3 sold)', 'url': 'https://www.ebay.com/sch/i.html?_nkw=' + (mpn or name)}

    # MPB (Stubbed)
    results['mpb'] = {'status': 'Used', 'price': '$2,780', 'url': 'https://www.mpb.com/en-us/'}

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

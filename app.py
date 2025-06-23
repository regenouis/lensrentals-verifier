from flask import Flask, request, render_template
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

def scrape_bh_by_mpn(mpn):
    search_url = f"https://www.bhphotovideo.com/c/search?Ntt={mpn}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.select("div#gridContent .itemBlock")

    if not products:
        return {
            'price': 'No match found',
            'url': search_url
        }

    for product in products[:3]:
        title_link = product.select_one("a.productListItem")
        if not title_link:
            continue
        product_url = "https://www.bhphotovideo.com" + title_link['href']

        prod_resp = requests.get(product_url, headers=headers)
        prod_soup = BeautifulSoup(prod_resp.text, "html.parser")

        mfr_line = prod_soup.find(text=lambda t: t and "MFR #" in t)
        if mfr_line and mpn.upper() in mfr_line:
            price_tag = prod_soup.select_one(".price_1DPoToKrLP8uWvruGqgtaY")
            price = price_tag.text.strip() if price_tag else "Price not listed"
            stock_tag = prod_soup.find("div", string=lambda s: s and "In Stock" in s)
            stock_status = "In Stock" if stock_tag else "Check availability"
            return {
                'price': f"{stock_status} — {price}",
                'url': product_url
            }

    return {
        'price': "⚠️ Multiple results — manual review",
        'url': search_url
    }

@app.route('/')
def home():
    return render_template('retail_price_viewer.html')

@app.route('/lookup', methods=['POST'])
def lookup():
    product_name = request.form.get('product_name', '').strip()
    mpn = request.form.get('mpn', '').strip()

    if not product_name and not mpn:
        return render_template('retail_price_viewer.html', error="Please enter either a product name or an MPN.")

    search_term = mpn if mpn else product_name
    encoded_search = search_term.replace(' ', '+')

    bh_result = scrape_bh_by_mpn(search_term)

    results = {
        'B&H Photo': bh_result,
        'Adorama': {
            'price': 'Out of Stock',
            'url': f'https://www.adorama.com/l/?searchinfo={encoded_search}'
        },
        'eBay Sold': {
            'price': '$2,950 avg (last 3 sold)',
            'url': f'https://www.ebay.com/sch/i.html?_nkw={encoded_search}&LH_Sold=1'
        },
        'MPB': {
            'price': 'Used — $2,780',
            'url': f'https://www.mpb.com/en-us/search/?q={encoded_search}'
        }
    }

    return render_template('retail_price_viewer.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, render_template
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def scrape_ebay_listings(query):
    try:
        url = f"https://www.ebay.com/sch/i.html?_nkw={query}&LH_ItemCondition=3000&_sop=12"
        response = requests.get(url, headers=HEADERS, timeout=6)
        soup = BeautifulSoup(response.text, 'html.parser')
        prices = [item.get_text() for item in soup.select("span.s-item__price")][:5]
        return prices if prices else None
    except:
        return None

def scrape_ebay_sold(query):
    try:
        url = f"https://www.ebay.com/sch/i.html?_nkw={query}&LH_Sold=1&LH_Complete=1"
        response = requests.get(url, headers=HEADERS, timeout=6)
        soup = BeautifulSoup(response.text, 'html.parser')
        prices = [item.get_text() for item in soup.select("span.s-item__price")][:3]
        return prices if prices else None
    except:
        return None

def scrape_mpb(query):
    try:
        url = f"https://www.mpb.com/en-us/search/?q={query}"
        response = requests.get(url, headers=HEADERS, timeout=6)
        soup = BeautifulSoup(response.text, 'html.parser')
        match = soup.select_one(".listing .price")
        return match.get_text(strip=True) if match else None
    except:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    data = {
        "name": "",
        "mpn": "",
        "adorama": "Check site manually",
        "ebay_for_sale": "No listings found",
        "ebay_sold": "No sold data",
        "mpb": "No data found",
        "ebay_for_sale_link": "",
        "ebay_sold_link": "",
        "mpb_link": "",
        "error": None
    }

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        mpn = request.form.get('mpn', '').strip()

        if not name and not mpn:
            data['error'] = "Please enter either a product name or MPN."
        else:
            query_param = mpn or name
            query_encoded = query_param.replace(' ', '+')

            data["name"] = name
            data["mpn"] = mpn

            # eBay links
            data['ebay_for_sale_link'] = f"https://www.ebay.com/sch/i.html?_nkw={query_encoded}&LH_ItemCondition=3000&_sop=12"
            data['ebay_sold_link'] = f"https://www.ebay.com/sch/i.html?_nkw={query_encoded}&LH_Sold=1&LH_Complete=1"

            # MPB link
            data['mpb_link'] = f"https://www.mpb.com/en-us/search/?q={query_encoded}"

            # Try to scrape
            for_sale = scrape_ebay_listings(query_encoded)
            data['ebay_for_sale'] = ', '.join(for_sale) if for_sale else "No listings found"

            sold = scrape_ebay_sold(query_encoded)
            data['ebay_sold'] = ', '.join(sold) if sold else "No sold data"

            mpb_price = scrape_mpb(query_encoded)
            data['mpb'] = mpb_price if mpb_price else "No data found"

    return render_template('retail_price_viewer.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

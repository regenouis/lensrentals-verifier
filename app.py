from flask import Flask, request, render_template
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import traceback

app = Flask(__name__)
CORS(app)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def scrape_ebay_listings(query):
    url = f"https://www.ebay.com/sch/i.html?_nkw={query}&LH_ItemCondition=3000&_sop=12"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    prices = [item.get_text() for item in soup.select("span.s-item__price")][:5]
    return prices

def scrape_ebay_sold(query):
    url = f"https://www.ebay.com/sch/i.html?_nkw={query}&LH_Sold=1&LH_Complete=1"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    prices = [item.get_text() for item in soup.select("span.s-item__price")][:3]
    return prices

def scrape_mpb(query):
    url = f"https://www.mpb.com/en-us/search/?q={query}"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    match = soup.select_one(".listing .price")
    return match.get_text(strip=True) if match else "No data found"

@app.route('/', methods=['GET', 'POST'])
def index():
    data = {
        "adorama": None,
        "ebay_for_sale": None,
        "ebay_sold": None,
        "mpb": None,
        "error": None,
        "ebay_for_sale_link": None,
        "ebay_sold_link": None,
        "mpb_link": None
    }

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        mpn = request.form.get('mpn', '').strip()

        if not name and not mpn:
            data['error'] = 'Please enter either a product name or MPN.'
        else:
            query_param = mpn or name
            ebay_query = query_param.replace(' ', '+')

            try:
                for_sale_prices = scrape_ebay_listings(ebay_query)
                data['ebay_for_sale'] = ', '.join(for_sale_prices) if for_sale_prices else 'No listings found'
            except Exception:
                data['ebay_for_sale'] = 'Error fetching eBay listings'

            try:
                sold_prices = scrape_ebay_sold(ebay_query)
                data['ebay_sold'] = ', '.join(sold_prices) if sold_prices else 'No sold data'
            except Exception:
                data['ebay_sold'] = 'Error fetching eBay sold data'

            try:
                data['mpb'] = scrape_mpb(query_param)
            except Exception:
                data['mpb'] = 'Error fetching MPB data'

            # Adorama static placeholder
            data['adorama'] = 'Check site manually'

            data['ebay_for_sale_link'] = f"https://www.ebay.com/sch/i.html?_nkw={ebay_query}&LH_ItemCondition=3000&_sop=12"
            data['ebay_sold_link'] = f"https://www.ebay.com/sch/i.html?_nkw={ebay_query}&LH_Sold=1&LH_Complete=1"
            data['mpb_link'] = f"https://www.mpb.com/en-us/search/?q={query_param}"

    try:
        return render_template('retail_price_viewer.html', data=data)
    except Exception as e:
        print("Template render failed:", str(e))
        print(traceback.format_exc())
        return f"Template render error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)

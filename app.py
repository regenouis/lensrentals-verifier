from flask import Flask, request, render_template
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

app = Flask(__name__)
CORS(app)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36"
}

def scrape_ebay_for_sale(mpn):
    query = quote_plus(mpn)
    url = f"https://www.ebay.com/sch/i.html?_nkw={query}&_sacat=0&LH_ItemCondition=3000&LH_BIN=1&rt=nc"
    try:
        r = requests.get(url, headers=HEADERS, timeout=8)
        soup = BeautifulSoup(r.text, 'html.parser')
        prices = [float(p.text.replace('$','').replace(',','')) for p in soup.select('.s-item__price')[:5] if '$' in p.text]
        avg_price = f"${sum(prices)/len(prices):,.2f}" if prices else "No matches"
        return avg_price, url
    except Exception as e:
        return "Error retrieving", url

def scrape_ebay_sold(mpn):
    query = quote_plus(mpn)
    url = f"https://www.ebay.com/sch/i.html?_nkw={query}&LH_Complete=1&LH_Sold=1"
    try:
        r = requests.get(url, headers=HEADERS, timeout=8)
        soup = BeautifulSoup(r.text, 'html.parser')
        prices = [float(p.text.replace('$','').replace(',','')) for p in soup.select('.s-item__price')[:5] if '$' in p.text]
        avg_price = f"${sum(prices)/len(prices):,.2f}" if prices else "No matches"
        return avg_price, url
    except Exception as e:
        return "Error retrieving", url

def scrape_mpb(mpn):
    query = quote_plus(mpn)
    url = f"https://www.mpb.com/en-us/search/?q={query}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=8)
        soup = BeautifulSoup(r.text, 'html.parser')
        item = soup.find('p', class_='sc-dJjYzT jJigTJ')
        return item.text.strip() if item else "Not listed", url
    except:
        return "Error retrieving", url

def scrape_adorama(mpn):
    query = quote_plus(mpn)
    url = f"https://www.adorama.com/l/?searchinfo={query}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=8)
        soup = BeautifulSoup(r.text, 'html.parser')
        price = soup.select_one('.productPrice')
        return price.text.strip() if price else "Not listed", url
    except:
        return "Error retrieving", url

@app.route('/', methods=['GET', 'POST'])
def home():
    data = {
        'name': '',
        'mpn': '',
        'error': '',
        'ebay_for_sale': '',
        'ebay_sold': '',
        'mpb': '',
        'adorama': '',
        'ebay_for_sale_link': '',
        'ebay_sold_link': '',
        'mpb_link': '',
        'adorama_link': ''
    }

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        mpn = request.form.get('mpn', '').strip()

        if not name and not mpn:
            data['error'] = 'Please enter either a Product Name or MPN.'
            return render_template('retail_price_viewer.html', data=data)

        data['name'] = name
        data['mpn'] = mpn

        if mpn:
            data['ebay_for_sale'], data['ebay_for_sale_link'] = scrape_ebay_for_sale(mpn)
            data['ebay_sold'], data['ebay_sold_link'] = scrape_ebay_sold(mpn)
            data['mpb'], data['mpb_link'] = scrape_mpb(mpn)
            data['adorama'], data['adorama_link'] = scrape_adorama(mpn)

    return render_template('retail_price_viewer.html', data=data)

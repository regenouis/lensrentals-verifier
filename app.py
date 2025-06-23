from flask import Flask, render_template, request
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import requests
from difflib import SequenceMatcher

app = Flask(__name__)

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def fetch_bh_tiles(product_name, mpn=None, max_results=5):
    query = mpn or product_name
    search_url = f"https://www.bhphotovideo.com/c/search?q={quote_plus(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=15)
    except Exception as e:
        return {"status": "❌ Error fetching B&H", "error": str(e)}

    soup = BeautifulSoup(response.text, 'html.parser')
    tiles = soup.select("div[data-selenium='miniProductPage']")[:max_results]

    results = []
    for tile in tiles:
        title_tag = tile.select_one("span[data-selenium='miniProductPageProductName']")
        price_tag = tile.select_one("span[data-selenium='uppedDecimalPrice']") or tile.select_one("span[data-selenium='pricingPrice']")
        link_tag = tile.select_one("a[href]")

        title = title_tag.text.strip() if title_tag else "N/A"
        price = price_tag.text.strip() if price_tag else "N/A"
        link = f"https://www.bhphotovideo.com{link_tag['href']}" if link_tag else "N/A"

        score = similarity(title, mpn) if mpn else similarity(title, product_name)

        results.append({
            "title": title,
            "price": price,
            "link": link,
            "score": score
        })

    best = max(results, key=lambda r: r['score'], default=None)
    if best and best['score'] >= 0.75:
        return {
            "status": "🟢 Found",
            "title": best['title'],
            "price": best['price'],
            "link": best['link']
        }
    else:
        return {
            "status": "🟡 No confident match",
            "alternatives": results,
            "search_link": search_url
        }

@app.route('/')
def index():
    return render_template('retail_price_viewer.html')

@app.route('/lookup', methods=['POST'])
def lookup():
    product_name = request.form.get('product_name', '').strip()
    mpn = request.form.get('mpn', '').strip()

    results = {}

    if product_name or mpn:
        bh_result = fetch_bh_tiles(product_name, mpn)
        results["B&H"] = bh_result

        # Placeholders for future retailer integrations
        results["Adorama"] = {"status": "🔧 Coming soon"}
        results["eBay"] = {"status": "🔧 Coming soon"}
        results["MPB"] = {"status": "🔧 Coming soon"}
    else:
        results["error"] = "Please enter a product name or MPN."

    return render_template("retail_price_viewer.html", results=results)

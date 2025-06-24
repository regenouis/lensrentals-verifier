from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def fetch_bh_data(mpn, name):
    try:
        if not mpn and not name:
            return {"status": "error", "message": "MPN or name required", "link": "", "price": ""}

        query = mpn if mpn else name
        bh_link = f"https://www.bhphotovideo.com/c/search?Ntt={query}"

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.bhphotovideo.com/",
        }

        response = requests.get(bh_link, headers=headers, timeout=10)

        if response.status_code == 403:
            return {
                "status": "error",
                "message": f"403 Client Error: Forbidden for url: {bh_link}",
                "link": bh_link,
                "price": "",
            }

        soup = BeautifulSoup(response.text, "html.parser")
        product_card = soup.select_one(".productListingContainer__content")

        if product_card:
            price_tag = product_card.select_one(".price_1DPoToKrLP8uWvruGqgtaY")
            price = price_tag.text.strip() if price_tag else "Price not found"
            return {
                "status": "success",
                "price": price,
                "link": bh_link,
                "message": "",
            }
        else:
            return {
                "status": "error",
                "message": "No match found ⚠️",
                "link": bh_link,
                "price": "",
            }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error fetching B&H data: {e}",
            "link": f"https://www.bhphotovideo.com/c/search?Ntt={mpn or name}",
            "price": "",
        }

@app.route('/', methods=['GET', 'POST'])
def index():
    data = {
        "bh": None,
        "adorama": "Out of Stock",
        "ebay": "$2,950 avg (last 3 sold)",
        "mpb": "$2,780",
        "error": None,
    }

    if request.method == 'POST':
        name = request.form.get("name", "").strip()
        mpn = request.form.get("mpn", "").strip()

        if not name and not mpn:
            data["error"] = "Please enter either a product name or MPN."
        else:
            data["bh"] = fetch_bh_data(mpn, name)

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

app = Flask(__name__)

def scrape_bh_photo(product_name, mpn):
    search_url = f"https://www.bhphotovideo.com/c/search?Ntt={quote_plus(mpn)}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(search_url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        listings = soup.select(".item_block")
        for item in listings:
            mpn_tag = item.select_one(".item_mpn, .item-sku span")
            if mpn_tag and mpn in mpn_tag.text:
                price_tag = item.select_one(".price_1DPoToKrLP8uWvruGqgtaY")
                used_tag = item.select_one(".usedPrice")
                link_tag = item.find("a", href=True)

                price = price_tag.text.strip() if price_tag else "No price listed"
                used_price = used_tag.text.strip() if used_tag else None
                product_link = "https://www.bhphotovideo.com" + link_tag["href"] if link_tag else search_url

                return {
                    "price": price,
                    "used_price": used_price,
                    "link": product_link,
                    "warning": None
                }

        return {
            "price": "No match found",
            "used_price": None,
            "link": search_url,
            "warning": "⚠️"
        }

    except Exception as e:
        return {
            "price": "Error fetching price",
            "used_price": None,
            "link": search_url,
            "warning": f"(Error: {e})"
        }

@app.route("/", methods=["GET", "POST"])
def index():
    context = {}
    if request.method == "POST":
        name = request.form.get("product_name", "").strip()
        mpn = request.form.get("product_mpn", "").strip()

        context["product_name"] = name
        context["product_mpn"] = mpn

        if not name and not mpn:
            context["error"] = "Please enter a product name or MPN."
            return render_template("retail_price_viewer.html", **context)

        context["bh"] = scrape_bh_photo(name, mpn)
        context["adorama"] = {"price": "Out of Stock"}
        context["ebay"] = {"price": "$2,950 avg (last 3 sold)", "link": "#"}
        context["mpb"] = {"price": "$2,780", "link": "#"}

    return render_template("retail_price_viewer.html", **context)

if __name__ == "__main__":
    app.run(debug=True)

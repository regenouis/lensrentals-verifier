# scrapers/bh_scraper.py

import requests
from bs4 import BeautifulSoup

def check_bh(product_name, mpn):
    url = f"https://www.bhphotovideo.com/c/search?q={mpn}&sts=ma"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        product_tiles = soup.select("div#resultsList .itemContainer")

        if not product_tiles:
            return {
                "retailer": "B&H",
                "status": "Not Found",
                "product_name": product_name,
                "mpn": mpn,
                "url": url,
                "note": "No products found — manual check recommended.",
            }

        # Find tile matching exact MPN
        for tile in product_tiles:
            name = tile.select_one(".productTitle")
            price = tile.select_one(".price_1DPoToKrLP8uWvruGqgtaY")
            stock = tile.select_one(".stockStatus")

            return {
                "retailer": "B&H",
                "status": "Found",
                "product_name": name.text.strip() if name else "N/A",
                "mpn": mpn,
                "price": price.text.strip() if price else "N/A",
                "availability": stock.text.strip() if stock else "Unknown",
                "url": url
            }

        return {
            "retailer": "B&H",
            "status": "Multiple Matches",
            "product_name": product_name,
            "mpn": mpn,
            "url": url,
            "note": "Multiple listings found — refine search manually."
        }

    except Exception as e:
        return {
            "retailer": "B&H",
            "status": "Error",
            "product_name": product_name,
            "mpn": mpn,
            "error": str(e),
            "url": url,
        }

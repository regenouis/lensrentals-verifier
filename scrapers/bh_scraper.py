def check_bh(product_name, mpn):
    print(f"[DEBUG] Received product_name: {product_name}, mpn: {mpn}")
    # rest of function...


import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

def check_bh(mpns, product_name=None):
    results = []
    for mpn in mpns:
        search_url = f"https://www.bhphotovideo.com/c/search?q={mpn}&sts=ma"
        try:
            response = requests.get(search_url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            # Look for all search result blocks
            product_blocks = soup.select("div.resultItem") or soup.select("div#productListing div.item")

            best_match = None
            for block in product_blocks:
                href_tag = block.find("a", href=True)
                text = block.get_text().lower()

                if href_tag and (mpn.lower() in text or (product_name and product_name.lower() in text)):
                    best_match = "https://www.bhphotovideo.com" + href_tag["href"]
                    break

            # If no match found
            if not best_match:
                return {
                    "retailer": "B&H",
                    "status": "Not Found",
                    "product_name": product_name,
                    "mpn": mpn,
                    "url": search_url,
                    "note": "No matching product block found — manual check recommended."
                }

            # Follow product link
            prod_response = requests.get(best_match, headers=HEADERS, timeout=10)
            prod_soup = BeautifulSoup(prod_response.text, "html.parser")

            # Confirm MPN on product page
            full_text = prod_soup.get_text().lower()
            confirmed = mpn.lower() in full_text or (product_name and product_name.lower() in full_text)

            if not confirmed:
                return {
                    "retailer": "B&H",
                    "status": "Mismatch",
                    "product_name": product_name,
                    "mpn": mpn,
                    "url": best_match,
                    "note": "Product page reached but MPN not confirmed — manual validation advised."
                }

            # Attempt price + stock extraction
            price_tag = prod_soup.select_one("div#PriceBlock .price_1DPoToKrLP8uWvruGqgtaY") or \
                        prod_soup.select_one("div.price")
            price = price_tag.get_text(strip=True) if price_tag else "Unknown"

            stock_tag = prod_soup.find(string=re.compile("In Stock", re.I))
            stock_status = "In Stock" if stock_tag else "Check Availability"

            return {
                "retailer": "B&H",
                "status": "Found",
                "product_name": product_name,
                "mpn": mpn,
                "url": best_match,
                "price": price,
                "stock": stock_status,
                "note": "Match found via product page"
            }

        except Exception as e:
            return {
                "retailer": "B&H",
                "status": "Error",
                "product_name": product_name,
                "mpn": mpn,
                "url": search_url,
                "note": f"Exception occurred: {str(e)}"
            }

    return {
        "retailer": "B&H",
        "status": "Not Found",
        "product_name": product_name,
        "mpn": ", ".join(mpns),
        "url": search_url,
        "note": "No results after full scan"
    }

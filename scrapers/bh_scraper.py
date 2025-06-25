import requests
from bs4 import BeautifulSoup

def check_bh(product_name, mpn):
    base_url = "https://www.bhphotovideo.com"
    search_url = f"{base_url}/c/search?q={mpn}&sts=ma"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        product_blocks = soup.select("div[data-selenium='miniProductPageProduct']")
        for block in product_blocks[:3]:  # check top 3 results
            title_elem = block.select_one("span[data-selenium='miniProductPageProductName']")
            mpn_elem = block.select_one("div[data-selenium='miniProductPageModel']")

            if title_elem and mpn_elem:
                title = title_elem.text.strip().lower()
                found_mpn = mpn_elem.text.strip().lower()
                if mpn.lower() in found_mpn and product_name.lower() in title:
                    price_elem = block.select_one("div[data-selenium='pricingPrice']")
                    status = "In Stock" if price_elem else "Possibly Out of Stock"

                    return {
                        "retailer": "B&H",
                        "status": status,
                        "product_name": product_name,
                        "mpn": mpn,
                        "url": search_url,
                        "note": "Match found via MPN and product name"
                    }

        return {
            "retailer": "B&H",
            "status": "Not Found",
            "product_name": product_name,
            "mpn": mpn,
            "url": search_url,
            "note": "No matching product block found — manual check recommended."
        }

    except Exception as e:
        return {
            "retailer": "B&H",
            "status": "Error",
            "product_name": product_name,
            "mpn": mpn,
            "url": search_url,
            "note": f"Scraper error: {str(e)}"
        }

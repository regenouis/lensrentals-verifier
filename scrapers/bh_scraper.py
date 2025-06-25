import requests
from bs4 import BeautifulSoup
import re

def check_bh(product_name, mpn):
    search_url = f"https://www.bhphotovideo.com/c/search?q={mpn}&sts=ma"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    result = {
        "retailer": "B&H",
        "status": "Not Found",
        "product_name": product_name,
        "mpn": mpn,
        "url": search_url,
        "note": "No products found — manual check recommended."
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        product_tiles = soup.select("div.item_wrapper")[:10]  # scan first 10

        for tile in product_tiles:
            # Try to extract MPN or Title
            title_elem = tile.select_one("span.description a")
            link_elem = title_elem.get("href") if title_elem else None
            title_text = title_elem.text.strip() if title_elem else ""
            raw_tile_html = str(tile)

            # Tier 1 check: exact MPN or fuzzy match in tile
            mpn_match = re.search(re.escape(mpn), raw_tile_html, re.IGNORECASE)
            name_match = product_name.lower() in title_text.lower()

            if mpn_match or name_match:
                # Follow link to product page
                product_url = f"https://www.bhphotovideo.com{link_elem}"
                product_page = requests.get(product_url, headers=headers, timeout=10)
                prod_soup = BeautifulSoup(product_page.text, "html.parser")

                # Parse real product details
                real_title = prod_soup.find("h1").text.strip()
                availability = prod_soup.select_one("div#stockStatus, div.availability, button.add-to-cart") or ""
                avail_text = availability.get_text(strip=True) if availability else "Status unknown"
                price_elem = prod_soup.select_one("span#priceToPayAmount")
                price = price_elem.text.strip() if price_elem else "N/A"

                # Confirm MPN match in spec table
                mpn_section = prod_soup.find(string=re.compile("MFR #"))
                page_mpn = mpn_section.find_next().text.strip() if mpn_section else ""

                if mpn.lower() in page_mpn.lower() or mpn_match:
                    result.update({
                        "status": "In Stock" if "stock" in avail_text.lower() else avail_text,
                        "url": product_url,
                        "note": f"Verified on product page: {avail_text}",
                        "price": price
                    })
                    return result

        return result  # Still not found after full scan
    except Exception as e:
        result["note"] = f"Scraper error: {e}"
        return result

import requests
from bs4 import BeautifulSoup

def check_bh(product_name, mpn):
    base_search_url = f"https://www.bhphotovideo.com/c/search?q={mpn}&sts=ma"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        # Step 1: Search B&H
        response = requests.get(base_search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        product_tiles = soup.find_all("div", class_="item-container")

        for tile in product_tiles:
            link_tag = tile.find("a", class_="photo")
            if not link_tag or not link_tag["href"]:
                continue

            product_url = "https://www.bhphotovideo.com" + link_tag["href"]

            # Step 2: Visit product page
            product_response = requests.get(product_url, headers=headers, timeout=10)
            product_soup = BeautifulSoup(product_response.text, "html.parser")

            # Step 3: Look for MPN on product page
            spec_table = product_soup.find("table", class_="specsTable")
            if spec_table:
                for row in spec_table.find_all("tr"):
                    label = row.fin

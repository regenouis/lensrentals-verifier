import requests
from bs4 import BeautifulSoup

def check_bh(mpn, product_name):
    result = {
        "retailer": "B&H",
        "status": "Not Found",
        "product_name": product_name,
        "mpn": mpn,
        "url": "",
        "note": ""
    }

    try:
        # Step 1: Search using product name (not MPN)
        search_query = product_name.replace(" ", "+")
        search_url = f"https://www.bhphotovideo.com/c/search?q={search_query}&sts=ma"
        result["url"] = search_url

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # Step 2: Find first matching product block
        product_blocks = soup.find_all("div", class_="item_block")
        for block in product_blocks:
            # Check for MPN match in data-description or similar tag
            if mpn.lower() in block.text.lower():
                link_tag = block.find("a", href=True)
                if link_tag:
                    product_page_url = f"https://www.bhphotovideo.com{link_tag['href']}"
                    result["status"] = "Found"
                    result["url"] = product_page_url
                    result["note"] = "Match found by product name and confirmed via MPN text match."
                    return result

        result["note"] = "No matching product block found — manual check recommended."

    except Exception as e:
        result["status"] = "Error"
        result["note"] = f"Exception occurred: {str(e)}"

    return result

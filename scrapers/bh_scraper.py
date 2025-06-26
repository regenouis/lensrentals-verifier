import requests
from bs4 import BeautifulSoup
import streamlit as st

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
        # Step 1: Construct search URL
        search_query = product_name.replace(" ", "+")
        search_url = f"https://www.bhphotovideo.com/c/search?q={search_query}&sts=ma"
        result["url"] = search_url

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # Step 2: Show snippet for visual debugging
        raw_html = soup.prettify()
        st.expander("🔍 Debug: Raw HTML Snippet").code(raw_html[:3000], language="html")

        # Step 3: Try alternative selectors if item_block not found
        possible_blocks = soup.select("div[class*='product'], div[data-selenium='miniProductPageProduct']")

        if not possible_blocks:
            result["note"] = "No known product blocks found — structure may have changed."
            return result

        for block in possible_blocks:
            block_text = block.get_text().lower()
            if mpn.lower() in block_text:
                link_tag = block.find("a", href=True)
                if link_tag:
                    result["status"] = "Found"
                    result["url"] = f"https://www.bhphotovideo.com{link_tag['href']}"
                    result["note"] = "Match found using fallback product block logic."
                    return result

        result["note"] = "MPN not found in fallback product blocks — try manual check."

    except Exception as e:
        result["status"] = "Error"
        result["note"] = f"Exception occurred: {str(e)}"

    return result

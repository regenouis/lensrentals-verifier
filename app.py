import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="Lensrentals Product Verifier", layout="centered")

st.title("🔍 Lensrentals Product Verifier")
st.markdown("Check product availability, pricing trends, and used value insights from top retailers.")

# --- INPUTS ---
product_name = st.text_input("📦 Product Name (with mount type)", "")
mpn = st.text_input("🔢 Manufacturer Part Number (optional)", "").strip()

if st.button("Run Verification") and product_name:
    # --- SEARCH B&H ---
    st.subheader("🛒 B&H Retail Search")
    query = '+'.join(product_name.split())
    bh_search_url = f"https://www.bhphotovideo.com/c/search?Ntt={query}&N=0&InitialSearch=yes"
    headers = {"User-Agent": "Mozilla/5.0"}
    bh_result = requests.get(bh_search_url, headers=headers)
    soup = BeautifulSoup(bh_result.text, 'html.parser')

    product_link = None
    for a in soup.find_all("a", href=True):
        href = a['href']
        text = a.get_text(strip=True)
        if product_name.lower() in text.lower():
            product_link = f"https://www.bhphotovideo.com{href}"
            break

    if product_link:
        prod_page = requests.get(product_link, headers=headers)
        prod_soup = BeautifulSoup(prod_page.text, 'html.parser')

        if mpn:
            found_mpn = prod_soup.find(string=re.compile(rf"\b{mpn}\b", re.IGNORECASE))
            if not found_mpn:
                st.error("❌ MPN not found on B&H product page. Aborting match.")
            else:
                bh_status = prod_soup.find("div", class_="stockStatus")
                status_text = bh_status.get_text(strip=True) if bh_status else "⚠️ Needs manual review"
                price_tag = prod_soup.find("span", class_="price_1DPoToKrLP8uWvruGqgtaY")
                price = price_tag.get_text(strip=True) if price_tag else "N/A"

                st.markdown(f"**B&H Link:** [View Product]({product_link})")
                st.markdown(f"**B&H Status:** {status_text}")
                st.markdown(f"**B&H Price:** {price}")
        else:
            bh_status = prod_soup.find("div", class_="stockStatus")
            status_text = bh_status.get_text(strip=True) if bh_status else "⚠️ Needs manual review"
            price_tag = prod_soup.find("span", class_="price_1DPoToKrLP8uWvruGqgtaY")
            price = price_tag.get_text(strip=True) if price_tag else "N/A"

            st.markdown(f"**B&H Link:** [View Product]({product_link})")
            st.markdown(f"**B&H Status:** {status_text}")
            st.markdown(f"**B&H Price:** {price}")
    else:
        st.warning("🔍 B&H product not found.")

    # --- Placeholder for next store expansion ---
    st.divider()
    st.caption("Adorama, eBay, and MPB data integration coming in next release.")

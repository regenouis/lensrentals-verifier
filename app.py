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
    st.subheader("🛒 B&H Retail Search")
    query = '+'.join(product_name.split())
    bh_search_url = f"https://www.bhphotovideo.com/c/search?Ntt={query}&N=0&InitialSearch=yes"
    headers = {"User-Agent": "Mozilla/5.0"}
    bh_result = requests.get(bh_search_url, headers=headers)
    soup = BeautifulSoup(bh_result.text, 'html.parser')

    st.markdown(f"🔗 [View B&H search results]({bh_search_url})")

    result_links = []
    for a in soup.find_all("a", href=True):
        href = a['href']
        text = a.get_text(strip=True).lower()
        if "/c/product/" in href and (
            product_name.lower() in text
            or (mpn and mpn.lower() in href.lower())
            or len(text) > 0
        ):
            full_url = f"https://www.bhphotovideo.com{href}"
            if full_url not in result_links:
                result_links.append(full_url)
        if len(result_links) >= 3:
            break

    product_found = False
    for link in result_links:
        prod_page = requests.get(link, headers=headers)
        prod_soup = BeautifulSoup(prod_page.text, 'html.parser')

        # MPN check
        if mpn:
            full_text = prod_soup.get_text().lower()
            meta_mpn = prod_soup.find("meta", attrs={"name": "productPartNumber"})
            found_mpn = mpn.lower() in full_text or (meta_mpn and mpn.lower() in meta_mpn.get("content", "").lower())
            if not found_mpn:
                continue
            mpn_verified = True
        else:
            mpn_verified = False

        # Get availability and price
        bh_status = prod_soup.find("div", class_="stockStatus")
        status_text = bh_status.get_text(strip=True) if bh_status else "⚠️ Needs manual review"
        price_tag = prod_soup.find("span", class_="price_1DPoToKrLP8uWvruGqgtaY")
        price = price_tag.get_text(strip=True) if price_tag else "N/A"

        st.markdown(f"**B&H Link:** [View Product]({link})")
        st.markdown(f"**B&H Status:** {status_text}")
        st.markdown(f"**B&H Price:** {price}")
        if mpn and not mpn_verified:
            st.markdown("⚠️ MPN not confirmed on page. Match appears accurate, but verify manually.")
        elif not mpn:
            st.markdown("⚠️ MPN not supplied. Displaying top result from B&H search.")
        product_found = True
        break

    if not product_found:
        st.warning("🔍 B&H product not found or MPN mismatch.")

    st.divider()
    st.caption("Now includes metadata MPN matching, softened product name logic, and top-result fallback.")

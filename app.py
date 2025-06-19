import streamlit as st
import requests
from bs4 import BeautifulSoup
import json

st.set_page_config(page_title="Lensrentals Product Verifier", layout="centered")
st.title("🔍 Lensrentals Product Verifier")
st.markdown("Check product availability, pricing trends, and used value insights from top retailers.")

# Inputs
product_name = st.text_input("📦 Product Name (with mount type)")
mpn_input = st.text_input("🔢 Manufacturer Part Number (optional)")

if st.button("Run Verification") and product_name.strip():
    st.subheader("🛒 B&H Retail Search")

    query = '+'.join(product_name.strip().split())
    bh_search_url = f"https://www.bhphotovideo.com/c/search?Ntt={query}&N=0&InitialSearch=yes"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(bh_search_url, headers=headers)

    st.markdown(f"🔗 [View B&H search results]({bh_search_url})")

    if response.status_code != 200:
        st.error("❌ Failed to fetch B&H page.")
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        result_links = []
        seen = set()

        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "/c/product/" in href and href not in seen:
                full_url = f"https://www.bhphotovideo.com{href}"
                seen.add(href)
                result_links.append(full_url)
            if len(result_links) >= 3:
                break

        found = False
        for link in result_links:
            page = requests.get(link, headers=headers)
            prod_soup = BeautifulSoup(page.text, "html.parser")

            matched = False
            for script in prod_soup.find_all("script", type="application/ld+json"):
                try:
                    data = json.loads(script.string.strip())
                    if isinstance(data, dict) and "mpn" in data:
                        if mpn_input:
                            if data["mpn"].lower() == mpn_input.lower():
                                matched = True
                                break
                        else:
                            matched = True
                            break
                except:
                    continue

            if matched:
                price_tag = prod_soup.find("span", class_="price_1DPoToKrLP8uWvruGqgtaY")
                price = price_tag.text.strip() if price_tag else "N/A"
                st.success(f"✅ Product Found: [View Product]({link})")
                st.markdown(f"**MPN Match:** `{mpn_input}`")
                st.markdown(f"**Price:** {price}")
                found = True
                break

        if not found:
            st.warning("🔍 B&H product not found or MPN mismatch.")

    st.caption("Now includes metadata MPN matching and fallback logic.")

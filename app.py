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

if st.button("Run Verification"):
    if not (product_name.strip() or mpn_input.strip()):
        st.warning("⚠️ Please enter at least a product name or manufacturer part number.")
    else:
        st.subheader("🛒 B&H Retail Search")
        headers = {"User-Agent": "Mozilla/5.0"}

        # Prefer MPN for search if present
        if mpn_input.strip():
            bh_search_url = f"https://www.bhphotovideo.com/c/search?q={mpn_input.strip()}"
        else:
            query = '+'.join(product_name.strip().split())
            bh_search_url = f"https://www.bhphotovideo.com/c/search?Ntt={query}&N=0&InitialSearch=yes"

        st.markdown(f"🔗 [View B&H search results]({bh_search_url})")

        try:
            response = requests.get(bh_search_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            result_links = []
            seen = set()
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "/c/product/" in href and href not in seen:
                    result_links.append(f"https://www.bhphotovideo.com{href}")
                    seen.add(href)
                if len(result_links) >= 3:
                    break

            found = False
            for link in result_links:
                prod_page = requests.get(link, headers=headers)
                prod_soup = BeautifulSoup(prod_page.text, "html.parser")
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
                    if mpn_input:
                        st.markdown(f"**MPN Match:** `{mpn_input}`")
                    st.markdown(f"**Price:** {price}")
                    found = True
                    break

            if not found:
                st.warning("🔍 B&H product not found or MPN mismatch.")
        except Exception as e:
            st.error("❌ Failed to fetch B&H page.")

        st.caption("Now supports MPN-only searches, fallback search logic, and validates input.")

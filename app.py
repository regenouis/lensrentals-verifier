import streamlit as st
import requests
from bs4 import BeautifulSoup
import json

st.set_page_config(page_title="Lensrentals Product Verifier", layout="centered")

st.markdown("# 🔍 Lensrentals Product Verifier")
st.markdown("Check product availability, pricing trends, and used value insights from top retailers.")

product_name = st.text_input("📦 Product Name (with mount type)", placeholder="e.g. Sony FE 24-70mm f/2.8 GM OSS II")
mpn = st.text_input("🧾 Manufacturer Part Number (optional)", placeholder="e.g. SEL70200GM2")

if st.button("Run Verification"):
    if not product_name and not mpn:
        st.warning("Please enter a product name, MPN, or both.")
    else:
        result = lookup_bh(product_name, mpn)
        st.markdown("## 🛒 B&H Retail Search")
        st.markdown(f"🔗 [View B&H search results]({result['link']})")

        if "🟢" in result["status"]:
            st.success(result["status"])
        elif "⚠️" in result["status"]:
            st.warning(result["status"])
        elif "🟡" in result["status"]:
            st.info(result["status"])
        else:
            st.error(result["status"])

        st.markdown("---")
        st.caption("Now supports MPN-only searches, fallback search logic, and validates input.")


def lookup_bh(product_name, mpn=None):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # Determine search query
    if mpn:
        query = mpn
    elif product_name:
        query = product_name
    else:
        return {
            "status": "❌ No input provided.",
            "link": "",
            "mpn_match": False
        }

    search_url = f"https://www.bhphotovideo.com/c/search?q={query}&sts=ma"
    manual_link = search_url

    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        if response.status_code != 200:
            return {
                "status": "❌ Failed to fetch B&H page.",
                "link": manual_link,
                "mpn_match": False
            }

        soup = BeautifulSoup(response.content, "html.parser")
        scripts = soup.find_all("script", type="application/ld+json")

        for script in scripts:
            if not script.string:
                continue
            try:
                data = json.loads(script.string.strip())
                if isinstance(data, dict) and "mpn" in data:
                    found_mpn = data["mpn"].strip().upper()
                    if mpn:
                        if found_mpn == mpn.upper():
                            return {
                                "status": "🟢 In Stock (MPN verified)",
                                "link": manual_link,
                                "mpn_match": True
                            }
                        else:
                            return {
                                "status": "⚠️ MPN mismatch — review manually.",
                                "link": manual_link,
                                "mpn_match": False
                            }
                    else:
                        return {
                            "status": "🟢 In Stock (via metadata match)",
                            "link": manual_link,
                            "mpn_match": True
                        }
            except json.JSONDecodeError:
                continue

        # No MPN found in metadata
        return {
            "status": "🟡 Metadata not found — manual review needed.",
            "link": manual_link,
            "mpn_match": False
        }

    except Exception as e:
        return {
            "status": f"❌ B&H fetch error: {str(e)}",
            "link": manual

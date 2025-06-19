import streamlit as st
import requests
from bs4 import BeautifulSoup
import json

st.set_page_config(page_title="Lensrentals Product Verifier", layout="centered")
st.markdown("# 🔍 Lensrentals Product Verifier")
st.markdown("Check product availability, pricing trends, and used value insights from top retailers.")

product_name = st.text_input("📦 Product Name (with mount type)", placeholder="e.g. Sony FE 24-70mm f/2.8 GM OSS II")
mpn = st.text_input("🧾 Manufacturer Part Number (optional)", placeholder="e.g. SEL70200GM2")

def lookup_bh(product_name, mpn=None):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    if mpn:
        query = mpn
    elif product_name:
        query = product_name
    else:
        return {
            "status": "❌ No input provided.",
            "link": "",
            "mpn_match": False,
            "error": True
        }

    search_url = f"https://www.bhphotovideo.com/c/search?q={query}&sts=ma"
    result = {
        "link": search_url,
        "status": "",
        "mpn_match": False,
        "error": False
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        if response.status_code != 200:
            result["status"] = f"❌ Failed to fetch B&H page (status {response.status_code})"
            result["error"] = True
            return result

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
                            result["status"] = "🟢 In Stock (MPN verified)"
                            result["mpn_match"] = True
                            return result
                        else:
                            result["status"] = f"⚠️ MPN mismatch — found `{found_mpn}`"
                            return result
                    else:
                        result["status"] = "🟢 In Stock (metadata present)"
                        result["mpn_match"] = True
                        return result
            except json.JSONDecodeError:
                continue

        # Page loaded, but no metadata matched
        result["status"] = "🟡 Metadata not found — review manually."
        return result

    except Exception as e:
        result["status"] = f"❌ Fetch error: {str(e)}"
        result["error"] = True
        return result

# UI logic
if st.button("Run Verification"):
    if not product_name and not mpn:
        st.warning("Please enter a product name, MPN, or both.")
    else:
        result = lookup_bh(product_name, mpn)
        st.markdown("## 🛒 B&H Retail Search")
        st.markdown(f"🔗 [View B&H search results]({result['link']})")

        if result["error"]:
            st.error(result["status"])
        elif "🟢" in result["status"]:
            st.success(result["status"])
        elif "⚠️" in result["status"]:
            st.warning(result["status"])
        elif "🟡" in result["status"]:
            st.info(result["status"])
        else:
            st.write(result["status"])

        st.markdown("---")
        st.caption("Now shows true fetch errors separately from metadata results.")

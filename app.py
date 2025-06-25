import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup

# Load API key from Streamlit Cloud secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Lensrentals Product Verifier", layout="wide")
st.title("🔍 Lensrentals Product Verifier")

product_name = st.text_input("Enter product name (e.g., 'Canon R5'):")
mpn = st.text_input("Enter MPN (Manufacturer Part Number):")

if st.button("Verify"):
    if not product_name or not mpn:
        st.warning("Please enter both a product name and MPN.")
    else:
        st.info("Verifying product...")

        # Example placeholder: Add your actual scraper function imports
        from scrapers.bh_scraper import check_bh
        from scrapers.adorama_scraper import check_adorama
        from scrapers.ebay_scraper import check_ebay
        from scrapers.mpb_scraper import check_mpb

        bh_data = check_bh(product_name, mpn)
        adorama_data = check_adorama(product_name, mpn)
        ebay_data = check_ebay(product_name, mpn)
        mpb_data = check_mpb(product_name, mpn)

        st.subheader("🔗 Availability & Pricing")

        st.write("### B&H")
        st.write(bh_data)

        st.write("### Adorama")
        st.write(adorama_data)

        st.write("### eBay (Used & Sold)")
        st.write(ebay_data)

        st.write("### MPB")
        st.write(mpb_data)

        st.success("Verification complete.")

import streamlit as st
from scrapers.bh_scraper import check_bh
from scrapers.ebay_scraper import check_ebay
from scrapers.adorama_scraper import check_adorama
from scrapers.mpb_scraper import check_mpb

st.set_page_config(page_title="Lensrentals Product Verifier", layout="centered")

st.markdown("## 🔍 Lensrentals Product Verifier")

product_name = st.text_input("Enter product name (e.g., 'Canon R5'):", "")
mpn = st.text_input("Enter MPN (Manufacturer Part Number):", "")

if st.button("Verify"):
    if not product_name or not mpn:
        st.error("Please enter both a product name and MPN.")
    else:
        with st.spinner("Verifying product..."):
            bh_data = check_bh(product_name, mpn)
            ebay_data = check_ebay(product_name, mpn)
            adorama_data = check_adorama(product_name, mpn)
            mpb_data = check_mpb(product_name, mpn)

            st.markdown("### 🔗 Availability & Pricing")

            for source in [bh_data, ebay_data, adorama_data, mpb_data]:
                with st.expander(source["retailer"]):
                    st.code(source, language="json")

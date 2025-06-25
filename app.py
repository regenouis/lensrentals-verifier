import streamlit as st
from scrapers.bh_scraper import check_bh

st.set_page_config(page_title="Lensrentals Product Verifier", layout="centered")

st.title("🔍 Lensrentals Product Verifier")

st.markdown(
    """
    Use this tool to check **real-time B&H availability and pricing** for a specific product.
    Enter the product name and its MPN (Manufacturer Part Number) below.
    """
)

with st.form("product_form"):
    product_name = st.text_input("Product Name", placeholder="e.g. Canon R5")
    mpn = st.text_input("MPN", placeholder="e.g. 4082C002")
    submitted = st.form_submit_button("Verify")

if submitted:
    if not product_name or not mpn:
        st.error("Please enter both the product name and MPN.")
    else:
        with st.spinner("Checking B&H Photo Video..."):
            bh_data = check_bh(mpn, product_name)  # ✅ Corrected argument order

        st.markdown("---")
        st.subheader("📦 B&H Result")
        if bh_data:
            st.json(bh_data)
        else:
            st.warning("No valid data returned from B&H. Please double-check the inputs.")

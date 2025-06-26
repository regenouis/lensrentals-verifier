import streamlit as st
from scrapers.bh_scraper import check_bh

st.title("🔍 Lensrentals Product Verifier")

st.markdown("""
Use this tool to check **real-time B&H availability** and **pricing** for a specific product.  
Enter the product name and its MPN (Manufacturer Part Number) below.
""")

with st.form("verify_form"):
    product_name = st.text_input("Product Name", placeholder="e.g., Canon EOS R50")
    mpn = st.text_input("MPN", placeholder="e.g., 5811C012")
    submitted = st.form_submit_button("Verify")

    if submitted:
        with st.spinner("Checking B&H..."):
            result = check_bh(product_name=product_name, mpn=mpn)
        st.markdown("### 📦 B&H Result")
        st.json(result)

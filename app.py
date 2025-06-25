import streamlit as st
from checker import check_bh  # Make sure your scraping logic is in checker.py

st.set_page_config(page_title="Product Verifier", layout="wide")

st.title("🔍 Lensrentals Product Verifier")
st.markdown("Use this tool to check **real-time B&H availability** and **pricing** for a specific product. "
            "Enter the product name and its MPN (Manufacturer Part Number) below.")

# Input fields
product_name = st.text_input("Product Name", placeholder="Canon EOS R50")
mpn = st.text_input("MPN", placeholder="5811C012")

if st.button("Verify"):
    with st.spinner("Checking B&H..."):
        result = check_bh(product_name=product_name, mpn=mpn)
        st.markdown("### 📦 B&H Result")
        st.json(result)

import streamlit as st

st.set_page_config(page_title="Lensrentals Verifier", layout="centered")
st.title("🔍 Lensrentals Product Verifier")

product_name = st.text_input("Enter product name (exact match)", "")

# Placeholder: Results frame with simulated better scraping logic
if product_name:
    st.subheader("Results (Simulated)")

    # Simulated logic test for Canon RF 24-70mm f/2.8L
    if "Canon RF 24-70mm f/2.8L" in product_name:
        st.markdown("**B&H Status:** 🟢 In Stock  \n🔗 [View on B&H](https://www.bhphotovideo.com/c/product/1504386-REG/canon_rf_24_70mm_f_2_8l_is.html)")
        st.markdown("**eBay Trend:** 🔴 Down ($2,200 → $1,800)  \n🔗 [View sold listings](https://www.ebay.com/sch/i.html?_nkw=Canon+RF+24-70mm+f%2F2.8L+IS+USM&LH_Sold=1&LH_Complete=1)")
        st.markdown("**MPB Price Range:** $1,959 – $2,189  \n🔗 [View on MPB](https://www.mpb.com/en-us/product/canon-rf-24-70mm-f-2-8-l-is-usm)")
        st.markdown("**Suggested Lensrentals Used Price:** ~$2,050")
    else:
        st.markdown("🔍 Enhanced lookup not yet implemented for this product.")

st.caption("Demo only: Full multi-vendor scraping and fuzzy matching logic coming in next deployment.")

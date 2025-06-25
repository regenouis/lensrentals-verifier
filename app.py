import streamlit as st
import openai
import pandas as pd
from dotenv import load_dotenv
import os

from scrapers.bh_scraper import get_bh_price
from scrapers.ebay_scraper import get_ebay_prices

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key securely
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Retail Price Verifier", layout="wide")
st.title("📦 Retail Price Verifier")

# Input field for product name/MPN
product_name = st.text_input("Enter Product Name or MPN", placeholder="Example: Nikon Zfc Mirrorless Camera (Silver)")

if product_name:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔍 B&H")
        bh_result = get_bh_price(product_name)
        st.write(bh_result)

    with col2:
        st.subheader("🛒 eBay")
        ebay_results = get_ebay_prices(product_name)
        df_ebay = pd.DataFrame(ebay_results)
        st.dataframe(df_ebay)

    st.markdown("---")
    st.subheader("🧠 GPT Summary")

    # GPT summary block
    if st.button("Generate GPT Summary"):
        context = f"B&H result: {bh_result}\n\nEbay results: {df_ebay.to_string(index=False)}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You're a retail analyst trained to summarize price insights for resale decision-making."},
                {"role": "user", "content": f"Summarize the pricing and availability insights for this product:\n\n{context}"}
            ],
            temperature=0.3,
            max_tokens=300
        )
        gpt_output = response.choices[0].message['content']
        st.text_area("GPT Summary", value=gpt_output, height=200)

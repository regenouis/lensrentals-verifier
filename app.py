
import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="Lensrentals Verifier", layout="centered")
st.title("🔍 Lensrentals Product Verifier")

product_name = st.text_input("Enter product name (exact match)", "")

def fetch_bh_status(product):
    url = f"https://www.bhphotovideo.com/c/search?Ntt={product.replace(' ', '%20')}&N=0&InitialSearch=yes"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        result_block = soup.find("div", class_="itemBlock")
        if not result_block:
            return "Not found", url
        stock = result_block.find("div", class_="stockStatus")
        if stock:
            text = stock.get_text(strip=True)
            if "In Stock" in text:
                return "In Stock", url
            elif "Backordered" in text:
                return "Backordered", url
            elif "Discontinued" in text:
                return "Discontinued", url
        return "Found, unknown status", url
    except Exception:
        return "Error fetching", url

def fetch_ebay_trend(product):
    url = f"https://www.ebay.com/sch/i.html?_nkw={product.replace(' ', '+')}&LH_Complete=1&LH_Sold=1"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        prices = soup.find_all("span", class_="s-item__price")
        values = []
        for p in prices[:5]:
            match = re.search(r'\$([0-9,.]+)', p.text)
            if match:
                price = float(match.group(1).replace(',', ''))
                values.append(price)
        if len(values) < 2:
            return "No trend data", url, "⚪"
        trend = "up" if values[0] > values[-1] else "down" if values[0] < values[-1] else "stable"
        color = {"up": "🟢", "down": "🔴", "stable": "⚪"}[trend]
        return f"{trend.title()} (${values[-1]} → ${values[0]})", url, color
    except Exception:
        return "Error fetching", url, "⚪"

if product_name:
    st.subheader("Results")

    with st.spinner("Checking B&H..."):
        bh_status, bh_url = fetch_bh_status(product_name)
        st.markdown(f"**B&H Status:** {bh_status}  
🔗 [View on B&H]({bh_url})")

    with st.spinner("Checking eBay sold listings..."):
        trend, ebay_url, emoji = fetch_ebay_trend(product_name)
        st.markdown(f"**eBay Trend:** {emoji} {trend}  
🔗 [View sold listings]({ebay_url})")

    if trend != "No trend data":
        suggested_prices = re.findall(r'\$([0-9,.]+)', trend)
        if suggested_prices:
            numeric_prices = [float(p) for p in suggested_prices]
            avg_price = int(sum(numeric_prices) / len(numeric_prices))
            st.markdown(f"**Suggested Lensrentals Used Price:** ~${avg_price}")

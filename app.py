from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

app = Flask(__name__)

def fetch_bh_price(mpn):
    try:
        # Headless Selenium browser setup
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

        search_url = f"https://www.bhphotovideo.com/c/search?Ntt={quote(mpn)}"
        driver.get(search_url)
        
        # Wait for page content
        driver.implicitly_wait(5)

        first_result = driver.find_elements(By.CSS_SELECTOR, 'div.productListing')[0]
        link_element = first_result.find_element(By.CSS_SELECTOR, 'a.link')
        price_element = first_result.find_element(By.CSS_SELECTOR, 'span[data-selenium="pricingPrice"]')

        product_url = link_element.get_attribute('href')
        price = price_element.text.strip()

        driver.quit()

        return {"status": "success", "price": price, "link": product_url}

    except Exception as e:
        return {"status": "error", "message": str(e), "link": f"https://www.bhphotovideo.com/c/search?Ntt={quote(mpn)}"}

def fetch_adorama():
    return "Out of Stock"

def fetch_ebay():
    return "$2,950 avg (last 3 sold)"

def fetch_mpb():
    return "$2,780"

@app.route("/", methods=["GET", "POST"])
def index():
    data = {}

    if request.method == "POST":
        name = request.form.get("name", "")
        mpn = request.form.get("mpn", "")

        if name.strip() == "" and mpn.strip() == "":
            data['error'] = "Please enter a product name or MPN."
            return render_template("retail_price_viewer.html", data=data)

        bh = fetch_bh_price(mpn.strip())
        data["bh"] = bh

        data["adorama"] = fetch_adorama()
        data["ebay"] = fetch_ebay()
        data["mpb"] = fetch_mpb()

    return render_template("retail_price_viewer.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)

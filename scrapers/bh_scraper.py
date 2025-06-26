from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import chromedriver_autoinstaller
import time

def check_bh(mpn, product_name):
    result = {
        "retailer": "B&H",
        "status": "Not Found",
        "product_name": product_name,
        "mpn": mpn,
        "url": "",
        "note": ""
    }

    # Auto-install compatible ChromeDriver
    chromedriver_autoinstaller.install()

    # Setup headless browser
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(options=options)
        search_query = product_name.replace(" ", "+")
        search_url = f"https://www.bhphotovideo.com/c/search?q={search_query}&sts=ma"
        result["url"] = search_url

        driver.get(search_url)
        time.sleep(2)  # Allow JavaScript to render

        product_blocks = driver.find_elements(By.CSS_SELECTOR, "div[data-selenium='miniProductPageProduct']")

        if not product_blocks:
            result["note"] = "No product blocks found — structure may have changed."
            return result

        for block in product_blocks:
            if mpn.lower() in block.text.lower():
                try:
                    link_tag = block.find_element(By.CSS_SELECTOR, "a")
                    href = link_tag.get_attribute("href")
                    result["status"] = "Found"
                    result["url"] = href
                    result["note"] = "Match found using MPN in Selenium-rendered block."
                    break
                except NoSuchElementException:
                    continue

        if result["status"] != "Found":
            result["note"] = "MPN not found in Selenium-rendered product blocks."

    except Exception as e:
        result["status"] = "Error"
        result["note"] = f"Exception occurred: {str(e)}"

    finally:
        try:
            driver.quit()
        except:
            pass

    return result

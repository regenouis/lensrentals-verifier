import requests
from bs4 import BeautifulSoup

def check_bh(product_name, mpn):
    return {
        "retailer": "B&H",
        "status": "TEST OK",
        "product_name": product_name,
        "mpn": mpn,
        "url": "https://www.bhphotovideo.com/",
        "note": "Test stub successful"
    }

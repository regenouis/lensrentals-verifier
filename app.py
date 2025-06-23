from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('retail_price_viewer.html')

@app.route('/lookup', methods=['POST'])
def lookup():
    product_name = request.form.get('product_name', '').strip()
    mpn = request.form.get('mpn', '').strip()

    if not product_name:
        return render_template('retail_price_viewer.html', error="Product name is required.")

    # Simulated results — replace with your scraper logic
    results = {
        'B&H Photo': {
            'price': 'In Stock — $3,199.99',
            'url': 'https://www.bhphotovideo.com/'
        },
        'Adorama': {
            'price': 'Out of Stock',
            'url': 'https://www.adorama.com/'
        },
        'eBay Sold': {
            'price': '$2,950 avg (last 3 sold)',
            'url': 'https://www.ebay.com/'
        },
        'MPB': {
            'price': 'Used — $2,780',
            'url': 'https://www.mpb.com/'
        }
    }

    return render_template('retail_price_viewer.html', results=results)

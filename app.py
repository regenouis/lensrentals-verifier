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

    if not product_name and not mpn:
        return render_template(
            'retail_price_viewer.html',
            error="Please enter either a product name or an MPN."
        )

    search_term = mpn if mpn else product_name
    encoded_search = search_term.replace(' ', '+')

    results = {
        'B&H Photo': {
            'price': 'In Stock — $3,199.99',
            'url': f'https://www.bhphotovideo.com/c/search?Ntt={encoded_search}'
        },
        'Adorama': {
            'price': 'Out of Stock',
            'url': f'https://www.adorama.com/l/?searchinfo={encoded_search}'
        },
        'eBay Sold': {
            'price': '$2,950 avg (last 3 sold)',
            'url': f'https://www.ebay.com/sch/i.html?_nkw={encoded_search}&LH_Sold=1'
        },
        'MPB': {
            'price': 'Used — $2,780',
            'url': f'https://www.mpb.com/en-us/search/?q={encoded_search}'
        }
    }

    return render_template(
        'retail_price_viewer.html',
        results=results
    )

if __name__ == '__main__':
    app.run(debug=True)

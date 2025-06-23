from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('retail_price_viewer.html')

@app.route('/lookup', methods=['POST'])
def lookup():
    product_name = request.form.get('product_name', '')
    mpn = request.form.get('mpn', '')

    # Dummy result logic (replace with your real logic)
    results = {
        "B&H": {
            "status": "Found",
            "new_price": "$2,495",
            "used_price": "$2,199",
            "link": "https://www.bhphotovideo.com/"
        },
        "eBay": {
            "status": "No results",
            "new_price": None,
            "used_price": None,
            "link": None
        }
    }

    return render_template('retail_price_viewer.html', results=results)

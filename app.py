from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('retail_price_viewer.html')

@app.route('/lookup', methods=['POST'])
def lookup():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No JSON payload received'}), 400

    product_name = data.get('product_name', '').strip()
    mpn = data.get('mpn', '').strip()

    if not product_name or not mpn:
        return jsonify({'error': 'Both product name and MPN are required'}), 400

    # Dummy simulated results (replace with real scraping logic later)
    results = {
        'product_name': product_name,
        'mpn': mpn,
        'bh_photo': 'In Stock — $3,199.99',
        'adorama': 'Out of Stock',
        'ebay_sold': '$2,950 avg (last 3 sold)',
        'mpb': 'Used — $2,780'
    }

    return jsonify(results)

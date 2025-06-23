from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/lookup", methods=["GET"])
def lookup():
    product_name = request.args.get("product", "").strip()
    mpn = request.args.get("mpn", "").strip()

    if not product_name and not mpn:
        return jsonify({"error": "At least one search parameter must be provided"}), 400

    # Replace with your actual matching logic
    dummy_result = {
        "bh": {
            "status": "ok",
            "used_price": "$1,999",
            "new_price": "$2,499",
            "link": "https://www.bhphotovideo.com/some-listing"
        }
    }

    return jsonify(dummy_result)

if __name__ == "__main__":
    app.run(debug=True)

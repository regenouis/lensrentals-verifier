from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def retail_price_viewer():
    # Pass an empty results dict to prevent template errors
    return render_template("retail_price_viewer.html", results={})

@app.route("/lookup", methods=["POST"])
def lookup():
    data = request.get_json()
    product_name = data.get("product_name")
    mpn = data.get("mpn")

    # Replace with your actual backend URL or local logic
    backend_url = "https://verifier-backend-met4.onrender.com/lookup_bh"

    try:
        response = requests.post(backend_url, json={"product_name": product_name, "mpn": mpn})
        response.raise_for_status()
        results = response.json()
    except Exception as e:
        results = {"error": str(e)}

    # Send results to the same template
    return render_template("retail_price_viewer.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)

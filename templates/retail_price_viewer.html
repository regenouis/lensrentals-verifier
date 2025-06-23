<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Retail Price Verifier</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      padding: 2rem;
      background-color: #f9f9f9;
      color: #333;
    }
    h1 {
      text-align: center;
      color: #2c3e50;
    }
    .source-block {
      background: #ffffff;
      border-radius: 8px;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
      margin: 1.5rem auto;
      padding: 1rem 1.5rem;
      max-width: 700px;
    }
    .form-group {
      margin-bottom: 1rem;
    }
    label {
      display: block;
      margin-bottom: 0.5rem;
    }
    input {
      width: 100%;
      padding: 0.5rem;
      font-size: 1rem;
    }
    button {
      width: 100%;
      padding: 0.75rem;
      background-color: #2c3e50;
      color: white;
      font-size: 1rem;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
    .result {
      margin-top: 1.5rem;
    }
  </style>
</head>
<body>
  <h1>Retail Price Verifier</h1>
  <div class="source-block">
    <form method="POST" action="/lookup">
      <div class="form-group">
        <label for="product_name">Product Name</label>
        <input type="text" id="product_name" name="product_name" required>
      </div>
      <div class="form-group">
        <label for="mpn">MPN (Manufacturer Part Number)</label>
        <input type="text" id="mpn" name="mpn"> <!-- No longer required -->
      </div>
      <button type="submit">Check Prices</button>
    </form>

    {% if results %}
      <div class="result">
        {% for source, data in results.items() %}
          <h2>{{ source }}</h2>
          <p>Status: {{ data.status }}</p>
          {% if data.used_price %}
            <p>Used Price: {{ data.used_price }}</p>
          {% endif %}
          {% if data.new_price %}
            <p>New Price: {{ data.new_price }}</p>
          {% endif %}
          {% if data.link %}
            <p><a href="{{ data.link }}" target="_blank">View Listing</a></p>
          {% endif %}
        {% endfor %}
      </div>
    {% endif %}
  </div>
</body>
</html>

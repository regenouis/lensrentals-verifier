<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Lensrentals Product Verifier</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <script>
        function resetForm() {
            const form = document.getElementById("productForm");
            form.reset();
            document.getElementById("name").value = "";
            document.getElementById("mpn").value = "";
        }

        function autoResetOnDelete(id) {
            const input = document.getElementById(id);
            input.addEventListener("input", () => {
                if (input.value.trim() === "") {
                    input.value = "";
                }
            });
        }

        window.onload = function () {
            autoResetOnDelete("name");
            autoResetOnDelete("mpn");
        }
    </script>
</head>
<body class="bg-light">
<div class="container mt-5 p-4 bg-white rounded shadow-sm">
    <h3>🔍 Lensrentals Product Verifier</h3>
    <form id="productForm" method="post">
        <div class="form-row">
            <div class="form-group col-md-6">
                <input id="name" name="name" class="form-control" placeholder="e.g., Sony FX3" value="{{ request.form.get('name', '') }}">
            </div>
            <div class="form-group col-md-6">
                <input id="mpn" name="mpn" class="form-control" placeholder="e.g., 1671" value="{{ request.form.get('mpn', '') }}">
            </div>
        </div>
        <p class="text-muted">Enter a product name or MPN — one is required.</p>
        <button type="submit" class="btn btn-primary">Check Prices</button>
        <button type="button" class="btn btn-secondary" onclick="resetForm()">Reset</button>
    </form>

    {% if data.error %}
        <div class="alert alert-danger mt-4">{{ data.error }}</div>
    {% endif %}

    {% if data.bh or data.adorama or data.ebay or data.mpb %}
        <hr>
        <h5>📎 Pricing Summary</h5>

        <p><strong>B&H Photo:</strong>
            {% if data.bh.status == 'error' %}
                <a href="{{ data.bh.link }}" target="_blank">Error fetching price</a>
                <span class="text-warning"> ({{ data.bh.message }})</span>
            {% else %}
                <a href="{{ data.bh.link }}" target="_blank">{{ data.bh.price }}</a>
            {% endif %}
        </p>

        <p><strong>Adorama:</strong> {{ data.adorama }}</p>
        <p><strong>eBay Sold:</strong> <a href="#">{{ data.ebay }}</a></p>
        <p><strong>MPB:</strong> <a href="#">{{ data.mpb }}</a></p>
    {% endif %}
</div>
</body>
</html>

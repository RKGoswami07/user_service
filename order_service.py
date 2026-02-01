from flask import Flask, jsonify, render_template_string
import requests

app = Flask(__name__)

# CHANGE THIS TO VM-1 IP
USER_SERVICE_URL = "http://192.168.56.101:5000"

orders = [
    {"order_id": 101, "user_id": 1, "item": "Laptop"},
    {"order_id": 102, "user_id": 2, "item": "Phone"}
]

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Order Dashboard</title>
    <style>
        table {
            border-collapse: collapse;
            width: 60%;
        }
        th, td {
            border: 1px solid #333;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #eee;
        }
    </style>
</head>
<body>
    <h1>Orders</h1>
    <button onclick="loadOrders()">Load Orders</button>
    <br><br>
    <table id="ordersTable" style="display:none;">
        <thead>
            <tr>
                <th>Order ID</th>
                <th>Item</th>
                <th>User ID</th>
                <th>User Name</th>
            </tr>
        </thead>
        <tbody></tbody>
    </table>

    <script>
        function loadOrders() {
            fetch("/orders")
                .then(response => response.json())
                .then(data => {
                    const table = document.getElementById("ordersTable");
                    const tbody = table.querySelector("tbody");

                    tbody.innerHTML = ""; // clear old rows

                    data.forEach(order => {
                        const row = document.createElement("tr");

                        row.innerHTML = `
                            <td>${order.order_id}</td>
                            <td>${order.item}</td>
                            <td>${order.user_id}</td>
                            <td>${order.user ? order.user.name : "N/A"}</td>
                        `;

                        tbody.appendChild(row);
                    });

                    table.style.display = "table";
                })
                .catch(() => alert("Error loading orders"));
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/orders")
def get_orders():
    result = []

    for order in orders:
        r = requests.get(f"{USER_SERVICE_URL}/users/{order['user_id']}")
        order_copy = order.copy()
        order_copy["user"] = r.json() if r.status_code == 200 else None
        result.append(order_copy)

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

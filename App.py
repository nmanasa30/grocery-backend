from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------------- Products ----------------
products = [
    {"name":"Rice","price":60,"category":"grains"},
    {"name":"Corn Flour","price":50,"category":"grains"},
    {"name":"Freedom Oil","price":90,"category":"grains"},
    {"name":"Green Gram","price":68,"category":"grains"},
    {"name":"Red Gram","price":88,"category":"grains"},
    {"name":"Maida Flour","price":50,"category":"grains"},
    {"name":"Wheat Flour","price":55,"category":"grains"},
    {"name":"Sugar","price":55,"category":"grains"},
    {"name":"Sunflower Oil","price":160,"category":"grains"},
    {"name":"Tomato","price":40,"category":"vegetables"},
    {"name":"Onions","price":40,"category":"vegetables"},
    {"name":"Lays Chips","price":20,"category":"snacks"},
    {"name":"Andhra Mixture","price":70,"category":"snacks"},
    {"name":"Maggi Noodles","price":15,"category":"snacks"},
    {"name":"Milk","price":50,"category":"dairy"},
    {"name":"Good Day Biscuits","price":30,"category":"dairy"},
    {"name":"Dairy Milk Chocolate","price":40,"category":"dairy"},
    {"name":"Butter Cookies","price":50,"category":"dairy"},
    {"name":"Cake","price":40,"category":"snacks"},
    {"name":"Dark Fantasy","price":90,"category":"snacks"}
]

# ---------------- Users ----------------
users = [
    {"username": "manasan", "password": "123456"}
]

# ---------------- Orders ----------------
orders = []

# ---------------- Routes ----------------
@app.route('/')
def home():
    return "Backend is running successfully! 🚀"

@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = next((u for u in users if u["username"]==username and u["password"]==password), None)
    for user in users:
        if user['username']==username and user['password']==password:
            return jsonify({"status":"success","message":"Login successful"})
    return jsonify({"status":"error","message":"Invalid credentials"})

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if any(u["username"] == username for u in users):
        return jsonify({"status": "error", "message": "Username already exists"}), 400
    users.append({"username": username, "password": password})
    return jsonify({"status": "success", "message": "Signup successful", "username": username})

@app.route('/api/order', methods=['POST'])
def create_order():
    data = request.json
    if not data or "cart" not in data or "phoneNumber" not in data:
        return jsonify({"status": "error", "message": "Invalid order data"}), 400
    order = {
        "id": len(orders) + 1,
        "cart": data["cart"],
        "phoneNumber": data["phoneNumber"]
    }
    orders.append(order)
    print(f"New Order: {order}")
    return jsonify({"status": "success", "message": "Order received", "orderId": order["id"]})

@app.route('/createPayment', methods=['POST'])
def create_payment():
    data = request.json
    if not data or "amount" not in data or "orderId" not in data:
        return jsonify({"status": "error", "message": "Invalid payment data"}), 400
    payload = {
        "orderId": data["orderId"],
        "amount": data["amount"],
        "phoneNumber": data.get("phoneNumber", ""),
        "merchantId": "TEST_MERCHANT",
        "currency": "INR",
        "status": "INITIATED"
    }
    return jsonify(payload)

# ---------------- Main ----------------
if __name__ == '__main__':
    app.run(debug=True)

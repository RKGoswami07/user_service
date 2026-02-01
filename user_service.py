from flask import Flask, jsonify

app = Flask(__name__)

users = {
    1: {"id": 1, "name": "Alice"},
    2: {"id": 2, "name": "Bob"}
}

@app.route("/users/<int:user_id>")
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

@app.route("/health")
def health():
    return jsonify({"status": "User service running"})

if __name__ == "__main__":
    # IMPORTANT: bind to 0.0.0.0
    app.run(host="0.0.0.0", port=5000)

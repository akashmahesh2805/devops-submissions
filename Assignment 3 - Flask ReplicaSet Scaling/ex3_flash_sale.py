import random
import socket
from datetime import datetime

from flask import Flask, jsonify, request

app = Flask(__name__)

ITEMS = [
    "Smartphone",
    "Shoes",
    "Headphones",
    "Laptop",
]


@app.route("/")
def index():
    return jsonify({
        "message": "Welcome to Big Sale!",
        "pod": socket.gethostname(),
        "ts": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    })


@app.route("/buy")
def buy():
    user = request.args.get("user")
    if not user:
        user = f"user-{random.randint(1000, 9999)}"

    item = random.choice(ITEMS)
    return jsonify({
        "status": "success",
        "item": item,
        "user": user,
        "served_by_pod": socket.gethostname(),
        "time": datetime.now().strftime("%H:%M:%S"),
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "pod": socket.gethostname(),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

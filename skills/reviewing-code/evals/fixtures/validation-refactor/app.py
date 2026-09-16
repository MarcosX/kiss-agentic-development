from flask import Flask, request
from validator import validate_order

app = Flask(__name__)

MAX_RETRY_ATTEMPTS = 3


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    validate_order(data)
    return {"status": "created"}, 201


@app.route("/admin/orders", methods=["POST"])
def admin_create_order():
    data = request.get_json()
    validate_order(data)
    if not data.get("admin_token"):
        return {"error": "missing admin_token"}, 400
    return {"status": "created"}, 201
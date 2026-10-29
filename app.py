from flask import Flask, render_template, request, jsonify
import razorpay
import hmac
import hashlib

app = Flask(__name__)
client = razorpay.Client(
    "rzp_test_TtpcMK3ahyyHSA", "V9WTJipJMjxmi75rnH6RZGBm"
)


@app.route("/create-order", methods=["POST"])
def create_order():
    data = request.json
    # प्लांस की राशि (Paise में)
    plans = {
        "normal_monthly": {"amount": 10000, "desc": "Normal Monthly"},
        "normal_yearly": {"amount": 100000, "desc": "Normal Yearly"},
        "hard_monthly": {"amount": 20000, "desc": "Hard Monthly"},
        "hard_yearly": {"amount": 120000, "desc": "Hard Yearly"},
    }

    plan_type = data.get("plan_type")
    if plan_type not in plans:
        return jsonify({"status": "Invalid Plan"}), 400

    order_data = {
        "amount": plans[plan_type]["amount"],
        "currency": "INR",
        "receipt": data["receipt"],
        "notes": {"plan_description": plans[plan_type]["desc"]},
    }
    order = client.order.create(data=order_data)
    return jsonify(order)


@app.route("/verify-payment", methods=["POST"])
def verify_payment():
    data = request.json
    msg = f"{data['order_id']}|{data['payment_id']}"
    generated_signature = hmac.new(
        "V9WTJipJMjxmi75rnH6RZGBm".encode("utf-8"),
        msg.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    if hmac.compare_digest(generated_signature, data["signature"]):
        return jsonify({"status": "Payment Verified"})
    else:
        return jsonify({"status": "Invalid Signature"}), 400

@app.route("/")
def index():
    return render_template("index.html")
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
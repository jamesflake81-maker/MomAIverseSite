from flask_cors import CORS

from flask import Flask, jsonify
import stripe, os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

# Read the secret key from the .env file
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

YOUR_DOMAIN = "https://momaiverse.com"

@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "MomAIverse Starter Kit",
                            "description": "Your first AI-powered income path using free tools.",
                        },
                        "unit_amount": 2500,
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=f"{YOUR_DOMAIN}/success.html",
            cancel_url=f"{YOUR_DOMAIN}/cancel.html",
        )
        return jsonify({"url": checkout_session.url})
    except Exception as e:
        return jsonify(error=str(e)), 400

from flask import request

@app.route("/webhook", methods=["POST"])
def webhook_received():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        # Invalid payload
        return jsonify(success=False, error="Invalid payload"), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return jsonify(success=False, error="Invalid signature"), 400

    # Handle successful payment
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_email = session.get("customer_details", {}).get("email")

        # 🔐 TODO: trigger encrypted file + email delivery here
        print(f"✅ Payment received from: {customer_email}")

    return jsonify(success=True), 200

if __name__ == "__main__":
    app.run(port=4242)
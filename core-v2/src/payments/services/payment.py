# -*- coding: iso8859-15 -*-
import os
import sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, "../.."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

import stripe
from global_config import STRIPE_KEY, STRIPE_PRODUCT_ID, convert_keys_to_camel_case
from payments.http.validation import OneTimePurchaseInput, CreateSubscriptionInput


stripe.api_key = STRIPE_KEY

ACCEPT_TYPE = ["card"]
ACCEPT_CURRENCIES = ["usd"]


class PaymentService:
    def generate_card_token(self, card_number, exp_month, exp_year, cvc):
        """Generate card token"""
        data = stripe.Token.create(
            card={
                "number": str(card_number),
                "exp_month": int(exp_month),
                "exp_year": int(exp_year),
                "cvc": str(cvc),
            }
        )
        card_token = data["id"]

        return card_token

    def create_payment_charge(self, token_id, amount):
        """Create payment charge"""
        payment = stripe.Charge.create(
            amount=int(amount) * 100,  # convert amount to cents
            currency="usd",
            description="Example charge",
            source=token_id,
        )

        payment_check = payment["paid"]  # return True for payment

        return payment_check

    async def create_subscription_process(self, data: CreateSubscriptionInput):
        if data.type not in ACCEPT_TYPE:
            return {"success": False, "message": "Invalid payment type"}

        if data.type == "card":
            card_number = data.cardNumber
            card_exp_year = data.expYear
            card_exp_month = data.expMonth
            card_cvc = data.cvc
            amount = data.amount
            currency = data.currency

            payment_method = self.create_payment_card(
                card_number, card_exp_month, card_exp_year, card_cvc
            )
            customer = self.create_customer(data.email)
            price = self.create_price(amount, currency)
            subscription = self.create_subscription(
                payment_method.id, customer.id, price.id
            )

            return convert_keys_to_camel_case(
                {
                    "success": True,
                    "customerId": customer.id,
                    "subscriptionId": subscription.id,
                }
            )

    def create_subscription(self, payment_method_id, customer_id, price_id):
        stripe.PaymentMethod.attach(payment_method_id, customer=customer_id)

        stripe.Customer.modify(
            customer_id,
            invoice_settings={
                "default_payment_method": payment_method_id,
            },
        )

        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[
                {
                    "price": price_id,
                }
            ],
            expand=["latest_invoice.payment_intent"],
        )
        return subscription

    def get_subscription(self, subscription_id: str):
        subscription = stripe.Subscription.retrieve(subscription_id)
        return subscription

    async def cancel_subscription(self, subscription_id):
        """Cancel a subcription"""
        stripe.Subscription.delete(subscription_id)
        return {"success": True}

    def create_customer(self, email):
        """Create new customer"""
        customer = stripe.Customer.create(email=email)
        return customer

    async def update_email_customer(self, customer_id, email):
        """Update customer email"""
        stripe.Customer.modify(customer_id, email=email)
        return {"success": True}

    def create_payment_card(self, card_number, exp_month, exp_year, cvc):
        """Create payment by card"""
        payment_method = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": str(card_number),
                "exp_month": int(exp_month),
                "exp_year": int(exp_year),
                "cvc": str(cvc),
            },
        )
        return payment_method

    def create_price(self, unit_amount, currency):
        """Create new price"""
        price = stripe.Price.create(
            unit_amount=int(unit_amount) * 100,
            currency=str(currency),
            recurring={"interval": "year"},
            product=STRIPE_PRODUCT_ID,
        )
        return price

    async def one_time_purchase(self, data: OneTimePurchaseInput):
        card_number = data.cardNumber
        card_exp_year = data.expYear
        card_exp_month = data.expMonth
        card_cvc = data.cvc
        amount = data.amount

        card_token = self.generate_card_token(
            card_number, card_exp_month, card_exp_year, card_cvc
        )

        payment = self.create_payment_charge(card_token, amount)

        return {"success": True}

# -*- coding: iso8859-15 -*-
import os
import sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, '..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

import stripe
from config.settings import STRIPE_KEY, STRIPE_PRODUCT_ID


stripe.api_key = STRIPE_KEY

ACCEPT_TYPE = ['card']
ACCEPT_CURRENCIES = ['usd']


def generate_card_token(card_number, exp_month, exp_year, cvv):
    ''' Generate card token '''
    data = stripe.Token.create(
        card={
            "number": str(card_number),
            "exp_month": int(exp_month),
            "exp_year": int(exp_year),
            "cvc": str(cvv),
        })
    card_token = data['id']

    return card_token


def create_payment_charge(token_id, amount):
    ''' Create payment charge '''
    payment = stripe.Charge.create(
        amount=int(amount)*100,                  # convert amount to cents
        currency='usd',
        description='Example charge',
        source=token_id,
    )

    payment_check = payment['paid']    # return True for payment

    return payment_check


def create_subscription(payment_method_id, customer_id, price_id):
    ''' Create a subcription '''
    stripe.PaymentMethod.attach(payment_method_id, customer=customer_id)
    # Set the default payment method on the customer
    stripe.Customer.modify(customer_id,
                           invoice_settings={
                               'default_payment_method': payment_method_id,
                           },
                           )
    # Create the subscription
    # Subscribe the user to the subscription created
    subscription = stripe.Subscription.create(
        customer=customer_id,
        items=[{"price": price_id, }],
        expand=["latest_invoice.payment_intent"]
    )
    return subscription


def get_subscription(subscription_id):
    ''' Get subcription by id'''
    subscription = stripe.Subscription.retrieve(subscription_id)
    return subscription


def cancel_subscription(subscription_id):
    ''' Cancel a subcription '''
    deletedSubscription = stripe.Subscription.delete(subscription_id)
    return deletedSubscription


def create_customer(email):
    ''' Create new customer '''
    customer = stripe.Customer.create(email=email)
    return customer


def update_email_customer(customer_id, email):
    ''' Update customer email '''
    customer = stripe.Customer.modify(customer_id, email=email)
    return customer


def create_payment_card(card_number, exp_month, exp_year, cvv):
    ''' Create payment by card '''
    payment_method = stripe.PaymentMethod.create(
        type="card",
        card={
            "number": str(card_number),
            "exp_month": int(exp_month),
            "exp_year": int(exp_year),
            "cvc": str(cvv),
        })
    return payment_method


def create_price(unit_amount, currency):
    ''' Create new price '''
    price = stripe.Price.create(
        unit_amount=int(unit_amount)*100,
        currency=str(currency),
        recurring={"interval": "year"},
        product=STRIPE_PRODUCT_ID
    )
    return price


if __name__ == "__main__":
    print(stripe.Product.create(name="Upstage").id)

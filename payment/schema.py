# -*- coding: iso8859-15 -*-
import os
import sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, '..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)
    
import graphene
from config.project_globals import app
from config.settings import URL_PREFIX
from flask_graphql import GraphQLView
from flask_jwt_extended.view_decorators import jwt_required
from graphene import relay
from utils import graphql_utils

from payment.payment import (ACCEPT_TYPE, cancel_subscription, create_customer,
                             create_payment_card, create_payment_charge,
                             create_price, create_subscription,
                             generate_card_token, update_email_customer)



class CardAttribute(graphene.InputObjectType):
    card_number = graphene.String(description="Card number")
    exp_year = graphene.String(description="Expired year")
    exp_month = graphene.String(description="Expired month")
    cvc = graphene.String(description="Cvc number")
    amount = graphene.Float(description='Amount payment')
    currency = graphene.String(description='Currency payment')


class OneTimePurchase(graphene.Mutation):
    """Mutation to add card details."""
    success = graphene.Boolean()
    payment_done = graphene.Boolean()

    class Arguments:
        input = CardAttribute(required=True)

    # @jwt_required()
    def mutate(self, info, input):
        data = graphql_utils.input_to_dictionary(input)
        card_number = data['card_number']
        card_expyear = data['exp_year']
        card_expmonth = data['exp_month']
        card_cvc = data['cvc']
        amount = data['amount']
        print(card_number, card_expyear, card_expmonth, card_cvc, amount)

        tokenid = generate_card_token(
            card_number, card_expmonth, card_expyear, card_cvc)

        payment_done = create_payment_charge(tokenid, amount)

        return OneTimePurchase(success=True, payment_done=payment_done)


class CreateSubscription(graphene.Mutation):
    """Mutation to create a subcription payment"""
    success = graphene.Boolean()
    customer_id = graphene.String()
    subscription_id = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        type = graphene.String(required=True)
        card = CardAttribute()

    @jwt_required()
    def mutate(self, info, email, type, card):
        if type not in ACCEPT_TYPE:
            return CreateSubscription(success=False)

        if type == 'card':
            data = graphql_utils.input_to_dictionary(card)
            card_number = data['card_number']
            card_expyear = data['exp_year']
            card_expmonth = data['exp_month']
            card_cvc = data['cvc']
            amount = data['amount']
            currency = data['currency']
            payment_method = create_payment_card(
                card_number, card_expmonth, card_expyear, card_cvc)
            customer = create_customer(email)
            price = create_price(amount, currency)
            subscription = create_subscription(
                payment_method.id, customer.id, price.id)

            return CreateSubscription(success=True, customer_id=customer.id, subscription_id=subscription.id)


class CancelSubscription(graphene.Mutation):
    """Mutation to remove a subcription payment"""
    success = graphene.Boolean()
    subscription_id = graphene.String()

    class Arguments:
        subscription_id = graphene.String(required=True)

    @jwt_required()
    def mutate(self, info, subscription_id):
        deleted_subscription = cancel_subscription(subscription_id)

        return CancelSubscription(success=True, subscription_id=deleted_subscription.id)


class UpdateEmailCustomer(graphene.Mutation):
    """Mutation to remove a subcription payment"""
    success = graphene.Boolean()
    customer_id = graphene.String()

    class Arguments:
        customer_id = graphene.String(required=True)
        email = graphene.String(required=True)

    @jwt_required()
    def mutate(self, info, customer_id, email):
        customer = update_email_customer(customer_id, email)

        return UpdateEmailCustomer(success=True, customer_id=customer.id)


class Query(graphene.ObjectType):
    node = relay.Node.Field()


class Mutation(graphene.ObjectType):
    oneTimePurchase = OneTimePurchase.Field()
    createSubscription = CreateSubscription.Field()
    cancelSubscription = CancelSubscription.Field()
    updateEmailCustomer = UpdateEmailCustomer.Field()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
payment_schema = graphene.Schema(query=Query, mutation=Mutation)
app.add_url_rule(
    f'/{URL_PREFIX}payment_graphql/', view_func=GraphQLView.as_view(
        "payment_graphql", schema=payment_schema,
        graphiql=True
    )
)

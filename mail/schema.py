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
from flask import request
from flask_graphql import GraphQLView
from graphene import relay

from mail.mail_utils import (push_mail_info_to_queue, save_email_token_client,
                             valid_token)


class EmailAttribute(graphene.InputObjectType):
    sender = graphene.String(description="The email of the sender user.")
    password = graphene.String(description="The password of the sender email.")
    subject = graphene.String(description="The subject of the email.")
    body = graphene.String(
        description="The body of the email. HTML is allowed.")
    recipients = graphene.List(
        graphene.String, description="The recipients of the email")
    bcc = graphene.List(
        graphene.String, description="The bcc recipients of the email", default_value=[])
    cc = graphene.List(
        graphene.String, description="The cc recipients of the email", default_value=[])
    filenames = graphene.List(
        graphene.String, description="The attachments of the email", default_value=[])


class SendEmailExternal(graphene.Mutation):
    """Mutation to send email."""
    success = graphene.Boolean(description="True if the config was saved.")

    class Arguments:
        email_info = EmailAttribute(required=True)

    def mutate(self, info, email_info):
        token = request.headers.get('X-Email-Token')
        if not token:
            raise Exception('Missing X-Email-Token header')

        try:
            if not valid_token(token):
                raise Exception('Invalid X-Email-Token')
        except:
            raise Exception('Invalid X-Email-Token')

        # Push email to queue
        push_mail_info_to_queue(email_info)

        return SendEmailExternal(success=True)


class PostToken(graphene.Mutation):
    """Mutation to post email token from Upstage to accept request send email to Upstage."""
    success = graphene.Boolean(description="True if post token success.")

    class Arguments:
        token = graphene.String(required=True)

    def mutate(self, info, token):
        save_email_token_client(token)

        return PostToken(success=True)


class Query(graphene.ObjectType):
    node = relay.Node.Field()


class Mutation(graphene.ObjectType):
    sendEmailExternal = SendEmailExternal.Field()
    postToken = PostToken.Field()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
email_schema = graphene.Schema(query=Query, mutation=Mutation)
app.add_url_rule(
    f'/{URL_PREFIX}/email_graphql/', view_func=GraphQLView.as_view(
        "email_graphql", schema=email_schema,
        graphiql=True
    )
)

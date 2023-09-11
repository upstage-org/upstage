# -*- coding: iso8859-15 -*-
import os
import sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, "../.."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

import graphene
from core.project_globals import app
from config import URL_PREFIX
from flask import request
from flask_graphql import GraphQLView
from graphene import relay
from graphql.execution.executors.asyncio import AsyncioExecutor

from core.mail.mail_utils import (
    create_email,
    save_email_token_client,
    send,
    send_async,
    valid_token,
)


class EmailAttribute(graphene.InputObjectType):
    sender = graphene.String(description="The email of the sender user.")
    password = graphene.String(description="The password of the sender email.")
    subject = graphene.String(description="The subject of the email.")
    body = graphene.String(description="The body of the email. HTML is allowed.")
    recipients = graphene.List(
        graphene.String, description="The recipients of the email"
    )
    bcc = graphene.List(
        graphene.String, description="The bcc recipients of the email", default_value=[]
    )
    cc = graphene.List(
        graphene.String, description="The cc recipients of the email", default_value=[]
    )
    filenames = graphene.List(
        graphene.String, description="The attachments of the email", default_value=[]
    )


class SendEmailExternal(graphene.Mutation):
    """Mutation to send email."""

    success = graphene.Boolean(description="True if the config was saved.")

    class Arguments:
        email_info = EmailAttribute(required=True)

    @staticmethod
    async def mutate(self, info, email_info: EmailAttribute):
        token = request.headers.get("X-Email-Token")
        if not token:
            raise Exception("Missing X-Email-Token header")

        try:
            if not valid_token(token):
                raise Exception("Invalid X-Email-Token")
        except:
            raise Exception("Invalid X-Email-Token")

        msg = create_email(
            to=email_info.recipients,
            subject=email_info.subject,
            html=email_info.body,
            cc=email_info.cc,
            bcc=email_info.bcc,
            filenames=email_info.filenames,
            external=True,
        )
        await send_async(msg=msg)

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
    f"/{URL_PREFIX}/email_graphql/",
    view_func=GraphQLView.as_view(
        "email_graphql", schema=email_schema, graphiql=True, executor=AsyncioExecutor()
    ),
)

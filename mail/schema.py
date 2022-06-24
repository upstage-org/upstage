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
from user.models import ADMIN, SUPER_ADMIN
from user.user_utils import current_user

from mail.mail_utils import push_mail_info_to_queue


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


class SendEmail(graphene.Mutation):
    """Mutation to send email."""
    success = graphene.Boolean(description="True if the config was saved.")

    class Arguments:
        email_info = EmailAttribute(required=True)

    @jwt_required()
    def mutate(self, info, email_info):
        code, error, user, timezone = current_user()
        if not user.role in (ADMIN, SUPER_ADMIN) and not user.can_send_email:
            raise Exception("Send Email Permission denied")

        # Push email to queue
        push_mail_info_to_queue(email_info)

        return SendEmail(success=True)


class Query(graphene.ObjectType):
    node = relay.Node.Field()


class Mutation(graphene.ObjectType):
    sendEmail = SendEmail.Field()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
email_schema = graphene.Schema(query=Query, mutation=Mutation)
app.add_url_rule(
    f'/{URL_PREFIX}/email_graphql/', view_func=GraphQLView.as_view(
        "email_graphql", schema=email_schema,
        graphiql=True
    )
)

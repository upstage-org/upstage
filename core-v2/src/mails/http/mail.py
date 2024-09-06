from ariadne import MutationType, QueryType, make_executable_schema
from graphql import GraphQLError
from mails.graphql.mail import type_defs
from ariadne.asgi import GraphQL

from mails.helpers.mail import create_email, send_async, valid_token

query = QueryType()
mutation = MutationType()


@mutation.field("sendEmailExternal")
async def send_email_external(_, info, email_info):
    request = info.context["request"]
    token = request.headers.get("X-Email-Token")
    if not token:
        raise GraphQLError("Missing X-Email-Token header")

    try:
        if not valid_token(token):
            raise GraphQLError("Invalid X-Email-Token")
    except:
        raise GraphQLError("Invalid X-Email-Token")

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
    return {"success": True}


schema = make_executable_schema(type_defs, query, mutation)
mail_graphql_app = GraphQL(schema, debug=True)

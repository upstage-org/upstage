import os
import sys

# Always on top
app_dir = os.path.abspath(os.path.dirname(__file__))
prodder = os.path.abspath(os.path.join(app_dir, ".."))
sys.path.append(app_dir)
sys.path.append(prodder)

from ariadne import MutationType, QueryType, gql, make_executable_schema
from fastapi import FastAPI
from users.http.user import user_graphql_app
from authentication.http.authentication import auth_graphql_app
from studio.http.studio import (
    query as studio_query,
    mutation as studio_mutation,
)
from assets.http.asset import query as asset_query, mutation as asset_mutation
from studio.graphql.studio import type_defs as studio_type_defs
from mails.http.mail import mail_graphql_app
from ariadne.asgi import GraphQL


def config_graphql_endpoints(app: FastAPI):
    app.add_route("/api/user_graphql", user_graphql_app)
    app.add_websocket_route("/api/user_graphql", user_graphql_app)

    app.add_route("/api/auth_graphql", auth_graphql_app)
    app.add_websocket_route("/api/auth_graphql", auth_graphql_app)

    setup_studio_endpoint(app)

    app.add_route("/api/email_graphql", mail_graphql_app)
    app.add_websocket_route("/api/email_graphql", mail_graphql_app)


def setup_studio_endpoint(app: FastAPI):
    combined_query = QueryType()
    combined_mutation = MutationType()

    combined_query.set_field("hello", asset_query._resolvers["hello"])
    combined_query.set_field("whoami", studio_query._resolvers["whoami"])
    combined_query.set_field("adminPlayers", studio_query._resolvers["adminPlayers"])
    combined_mutation.set_field(
        "batchUserCreation", studio_mutation._resolvers["batchUserCreation"]
    )
    combined_mutation.set_field("uploadFile", asset_mutation._resolvers["uploadFile"])
    combined_schema = make_executable_schema(
        studio_type_defs, combined_query, combined_mutation
    )

    combined_graphql_app = GraphQL(combined_schema, debug=True)

    app.add_route("/api/studio_graphql", combined_graphql_app)
    app.add_websocket_route("/api/studio_graphql", combined_graphql_app)

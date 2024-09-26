import os
import sys

# Always on top
app_dir = os.path.abspath(os.path.dirname(__file__))
prodder = os.path.abspath(os.path.join(app_dir, ".."))
sys.path.append(app_dir)
sys.path.append(prodder)

from ariadne import MutationType, QueryType, make_executable_schema
from fastapi import FastAPI
from users.http.user import user_graphql_app
from authentication.http.authentication import auth_graphql_app
from studios.http.studio import (
    query as studio_query,
    mutation as studio_mutation,
)
from assets.http.asset import query as asset_query, mutation as asset_mutation
from studios.graphql.studio import type_defs as studio_type_defs
from mails.http.mail import mail_graphql_app
from stages.http.stage import stage_graphql_app
from licenses.http.license import license_graphql_app
from performance_config.http.performance import performance_graphql_app
from upstage_options.http.setting import config_graphql_app
from ariadne.asgi import GraphQL


def config_graphql_endpoints(app: FastAPI):
    app.add_route("/api/user_graphql", user_graphql_app)
    app.add_websocket_route("/api/user_graphql", user_graphql_app)

    app.add_route("/api/auth_graphql", auth_graphql_app)
    app.add_websocket_route("/api/auth_graphql", auth_graphql_app)

    setup_studio_endpoint(app)

    app.add_route("/api/stage_graphql", stage_graphql_app)
    app.add_websocket_route("/api/stage_graphql", stage_graphql_app)

    app.add_route("/api/email_graphql", mail_graphql_app)
    app.add_websocket_route("/api/email_graphql", mail_graphql_app)

    app.add_route("/api/license_graphql", license_graphql_app)
    app.add_websocket_route("/api/license_graphql", license_graphql_app)

    app.add_route("/api/performance_graphql", performance_graphql_app)
    app.add_websocket_route("/api/performance_graphql", performance_graphql_app)

    app.add_route("/api/config_graphql", config_graphql_app)
    app.add_websocket_route("/api/config_graphql", config_graphql_app)


def setup_studio_endpoint(app: FastAPI):
    combined_query = QueryType()
    combined_mutation = MutationType()

    combined_query.set_field("media", asset_query._resolvers["media"])
    combined_query.set_field("whoami", studio_query._resolvers["whoami"])
    combined_query.set_field("adminPlayers", studio_query._resolvers["adminPlayers"])
    combined_query.set_field("mediaList", asset_query._resolvers["mediaList"])
    combined_mutation.set_field(
        "batchUserCreation", studio_mutation._resolvers["batchUserCreation"]
    )
    combined_mutation.set_field("uploadFile", asset_mutation._resolvers["uploadFile"])
    combined_mutation.set_field("saveMedia", asset_mutation._resolvers["saveMedia"])
    combined_mutation.set_field("deleteMedia", asset_mutation._resolvers["deleteMedia"])
    combined_mutation.set_field("updateUser", studio_mutation._resolvers["updateUser"])
    combined_mutation.set_field("deleteUser", studio_mutation._resolvers["deleteUser"])
    combined_mutation.set_field("sendEmail", studio_mutation._resolvers["sendEmail"])
    combined_mutation.set_field(
        "changePassword", studio_mutation._resolvers["changePassword"]
    )
    combined_mutation.set_field("calcSizes", studio_mutation._resolvers["calcSizes"])
    combined_mutation.set_field(
        "requestPermission",
        studio_mutation._resolvers["requestPermission"],
    )
    combined_mutation.set_field(
        "confirmPermission",
        studio_mutation._resolvers["confirmPermission"],
    )
    combined_mutation.set_field(
        "quickAssignMutation",
        studio_mutation._resolvers["quickAssignMutation"],
    )
    combined_schema = make_executable_schema(
        studio_type_defs, combined_query, combined_mutation
    )

    combined_graphql_app = GraphQL(combined_schema, debug=True)

    app.add_route("/api/studio_graphql", combined_graphql_app)
    app.add_websocket_route("/api/studio_graphql", combined_graphql_app)

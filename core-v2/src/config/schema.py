from fastapi import FastAPI
from users.schemas.user import user_graphql_app


def config_graphql_endpoints(app: FastAPI):
    app.add_route("/user-graphql", user_graphql_app)
    app.add_websocket_route("/user-graphql", user_graphql_app)
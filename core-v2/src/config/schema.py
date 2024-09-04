import os
import sys

# Always on top
app_dir = os.path.abspath(os.path.dirname(__file__))
prodder = os.path.abspath(os.path.join(app_dir, ".."))
sys.path.append(app_dir)
sys.path.append(prodder)

from fastapi import FastAPI
from users.http.controllers.user import user_graphql_app
from authentication.http.controllers.authentication import auth_graphql_app


def config_graphql_endpoints(app: FastAPI):
    app.add_route("/api/user_graphql", user_graphql_app)
    app.add_websocket_route("/api/user_graphql", user_graphql_app)

    app.add_route("/api/auth_graphql", auth_graphql_app)
    app.add_websocket_route("/api/auth_graphql", auth_graphql_app)

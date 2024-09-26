from ariadne import MutationType, QueryType, make_executable_schema
from ariadne.asgi import GraphQL
from authentication.http.validation import LoginInput
from authentication.services.auth import AuthenticationService
from bootstraps import app
from core.decorators.authenticated import authenticated
from users.entities.user import UserEntity
from authentication.graphql.authentication import type_defs


query = QueryType()
mutation = MutationType()


@mutation.field("login")
async def login(
    _,
    info,
    payload: LoginInput,
    authentication_service: AuthenticationService = AuthenticationService(),
):
    return await authentication_service.login(
        LoginInput(**payload), info.context["request"]
    )


@mutation.field("refreshToken")
@authenticated()
def refresh_token(
    _,
    info,
    authentication_service: AuthenticationService = AuthenticationService(),
):
    return authentication_service.refresh_token(
        UserEntity(**info.context["request"].state.current_user),
        info.context["request"],
    )


@mutation.field("logout")
async def resolve_logout(
    _,
    info,
    authentication_service: AuthenticationService = AuthenticationService(),
):
    return await authentication_service.logout(info.context["request"])


schema = make_executable_schema(type_defs, query, mutation)
auth_graphql_app = GraphQL(schema, debug=True)

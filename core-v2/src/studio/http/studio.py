from typing import List
from ariadne import MutationType, QueryType, make_executable_schema
from core.decorators.authenticated import authenticated
from core.helpers.object import convert_keys_to_camel_case
from ariadne.asgi import GraphQL
from studio.graphql.studio import type_defs
from studio.http.validation import BatchUserInput
from studio.services.sudio import StudioService
from users.entities.user import ADMIN, ROLES, SUPER_ADMIN


query = QueryType()
mutation = MutationType()


@query.field("whoami")
@authenticated()
def current_user(_, info):
    user = info.context["request"].state.current_user
    return convert_keys_to_camel_case({**user, "roleName": ROLES[int(user["role"])]})


@query.field("adminPlayers")
@authenticated()
def admin_players(_, __, **kwargs):
    return StudioService().admin_players(kwargs)


@mutation.field("batchUserCreation")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN])
def create_users(_, __, users: List[BatchUserInput]):
    print(users)
    return StudioService().create_users(users)


schema = make_executable_schema(type_defs, query, mutation)
studio_graphql_app = GraphQL(schema, debug=True)

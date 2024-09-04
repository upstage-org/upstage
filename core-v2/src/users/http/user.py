from ariadne import MutationType, QueryType, make_executable_schema
from core.decorators.authenticated import authenticated
from core.helpers.object import convert_keys_to_camel_case
from users.graphql.user import type_defs
from ariadne.asgi import GraphQL

from users.http.validation import CreateUserInput
from users.services.user import UserService

query = QueryType()
mutation = MutationType()


@query.field("currentUser")
@authenticated()
def current_user(_, info):
    return convert_keys_to_camel_case(info.context["request"].state.current_user)


@mutation.field("createUser")
def create_user(_, info, inbound: CreateUserInput, user_service=UserService()):
    return user_service.create(inbound, info.context["request"])


schema = make_executable_schema(type_defs, query, mutation)
user_graphql_app = GraphQL(schema, debug=True)

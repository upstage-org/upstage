from ariadne import MutationType, QueryType, make_executable_schema
from users.graphql.user import type_defs
from ariadne.asgi import GraphQL

from users.http.dtos.signup import SignupDTO
from users.services.user import UserService

query = QueryType()
mutation = MutationType()


@query.field("hello")
def resolve_hello(*_):
    return {"res": [{"id": 1, "name": "Hello"}, {"id": 2, "name": "World"}]}


@mutation.field("createUser")
def create_user(_, info, inbound: SignupDTO, user_service=UserService()):
    return user_service.create(inbound, info.context["request"])


schema = make_executable_schema(type_defs, query, mutation)
user_graphql_app = GraphQL(schema, debug=True)

from ariadne import MutationType, QueryType, make_executable_schema
from core.decorators.authenticated import authenticated
from stages.graphql.stage import type_defs
from ariadne.asgi import GraphQL

from stages.http.validation import StageInput
from stages.services.stage import StageService
from users.entities.user import ADMIN, PLAYER, SUPER_ADMIN, UserEntity

query = QueryType()
mutation = MutationType()


@query.field("hello")
def hello(*_):
    return "Hello, world!"


@mutation.field("createStage")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN, PLAYER])
def create_stage(_, info, input):
    return StageService().create_stage(
        UserEntity(**info.context["request"].state.current_user), StageInput(**input)
    )


schema = make_executable_schema(type_defs, query, mutation)
stage_graphql_app = GraphQL(schema, debug=True)

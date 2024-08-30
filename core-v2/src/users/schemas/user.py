from ariadne import MutationType, QueryType, make_executable_schema
from users.graphql.user import type_defs
from users.resolvers.user import UserResolver
from ariadne.asgi import GraphQL
from fastapi import Depends

query = QueryType()
mutation = MutationType()


class UserSchema: 
    def __init__(self, user_resolver: UserResolver = Depends()):
        print(self)
        self.user_resolver = user_resolver
    
    @query.field("hello")
    def resolve_hello(self, *_):
        return 'Hello, world!'
    
    @mutation.field("createUser")
    def resolve_create_user(self, info, data):
        username = data.get("username")
        status = data.get("status", "Active")
        return {"username": username, "status": status}



schema = make_executable_schema(type_defs, query, mutation)
user_graphql_app = GraphQL(schema, debug=True)
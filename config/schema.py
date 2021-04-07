# -*- coding: iso8859-15 -*-
from config.project_globals import app
from flask_graphql import GraphQLView
from config.settings import VERSION
from graphene import relay
import graphene


class NginxConfig(graphene.ObjectType):
    uploadLimit = graphene.Int()

    def resolve_uploadLimit(self, info):
        nginx_config = 'system/dev/upstage.nginx'
        with open(nginx_config) as file:
            for line in file:
                line = line.strip().lower()
                if line.startswith('client_max_body_size'):
                    limit = line.split(' ')[1]
                    if limit.endswith(';'):
                        limit = limit[0:-1]
                    if limit.endswith('k'):
                        limit = int(limit[0:-1])*1024
                    if limit.endswith('m'):
                        limit = int(limit[0:-1])*1024*1024
        return limit


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    nginx = graphene.Field(NginxConfig)

    def resolve_nginx(self, info):
        return NginxConfig()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
config_schema = graphene.Schema(query=Query)
app.add_url_rule(
    f'/{VERSION}/config_graphql/', view_func=GraphQLView.as_view(
        "config_graphql", schema=config_schema,
        graphiql=True
    )
)

# -*- coding: iso8859-15 -*-
from os import name
from config.project_globals import ScopedSession, app
from flask_graphql import GraphQLView
from config.settings import VERSION
from graphene import relay
import graphene
from config.models import Config as ConfigModel

TERMS_OF_SERVICE = 'TERMS_OF_SERVICE'


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


class SystemConfig(graphene.ObjectType):
    termsOfService = graphene.String()

    def resolve_termsOfService(self, info):
        with ScopedSession() as local_db_session:
            config = local_db_session.query(ConfigModel).filter(
                ConfigModel.name == TERMS_OF_SERVICE
            ).first()
            if config:
                return config.value


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    nginx = graphene.Field(NginxConfig)
    system = graphene.Field(SystemConfig)

    def resolve_nginx(self, info):
        return NginxConfig()

    def resolve_system(self, info):
        return SystemConfig()


class UpdateTermsOfService(graphene.Mutation):
    """Mutation to update Terms of Service's URL."""
    url = graphene.String(description="The updated Terms of Service's URL.")

    class Arguments:
        url = graphene.String(required=True)

    # decorate this with jwt login decorator.
    def mutate(self, info, url):
        with ScopedSession() as local_db_session:
            config = local_db_session.query(ConfigModel).filter(
                ConfigModel.name == TERMS_OF_SERVICE
            ).first()
            if config:
                config.value = url
            else:
                config = ConfigModel(name=TERMS_OF_SERVICE, value=url)
                local_db_session.add(config)

            local_db_session.commit()

            return UpdateTermsOfService(url=url)


class Mutation(graphene.ObjectType):
    updateTermsOfService = UpdateTermsOfService.Field()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
config_schema = graphene.Schema(query=Query, mutation=Mutation)
app.add_url_rule(
    f'/{VERSION}/config_graphql/', view_func=GraphQLView.as_view(
        "config_graphql", schema=config_schema,
        graphiql=True
    )
)

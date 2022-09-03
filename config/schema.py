# -*- coding: iso8859-15 -*-
from os import name

from flask_jwt_extended.view_decorators import jwt_required
from config.project_globals import DBSession, ScopedSession, app
from flask_graphql import GraphQLView
from config.settings import NGINX_CONFIG_FILE, URL_PREFIX
from graphene import relay
import graphene
from config.models import Config as ConfigModel
from mail.mail_utils import send
from user.models import ADMIN, SUPER_ADMIN
from user.user_utils import current_user

TERMS_OF_SERVICE = 'TERMS_OF_SERVICE'
MANUAL = 'MANUAL'
EMAIL_SUBJECT_PREFIX = 'EMAIL_SUBJECT_PREFIX'


class NginxConfig(graphene.ObjectType):
    uploadLimit = graphene.Int()

    def resolve_uploadLimit(self, info):
        with open(NGINX_CONFIG_FILE) as file:
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


def get_config(name):
    config = DBSession.query(ConfigModel).filter(
        ConfigModel.name == name).first()
    if config:
        return config.value


class SystemConfig(graphene.ObjectType):
    termsOfService = graphene.String()
    manual = graphene.String()
    esp = graphene.String()

    def resolve_termsOfService(self, info):
        return get_config(TERMS_OF_SERVICE)

    def resolve_manual(self, info):
        return get_config(MANUAL)

    def resolve_esp(self, info):
        return get_config(EMAIL_SUBJECT_PREFIX)

class FoyerConfig(graphene.ObjectType):
    title = graphene.String()
    description = graphene.String()
    menu = graphene.String()
    showRegistration = graphene.Boolean()

    def resolve_title(self, info):
        return get_config('FOYER_TITLE')

    def resolve_description(self, info):
        return get_config('FOYER_DESCRIPTION')

    def resolve_menu(self, info):
        return get_config('FOYER_MENU')

    def resolve_showRegistration(self, info):
        return get_config('SHOW_REGISTRATION')

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    nginx = graphene.Field(NginxConfig)
    system = graphene.Field(SystemConfig)
    foyer = graphene.Field(FoyerConfig)

    def resolve_nginx(self, info):
        return NginxConfig()

    def resolve_system(self, info):
        return SystemConfig()

    def resolve_foyer(self, info):
        return FoyerConfig()


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


class SaveConfig(graphene.Mutation):
    """Mutation to customise foyer."""
    success = graphene.Boolean(description="True if the config was saved.")

    class Arguments:
        name = graphene.String(
            required=True, description="The name of the config.")
        value = graphene.String(
            required=True, description="The value of the config.")

    # decorate this with jwt login decorator.
    def mutate(self, info, name, value):
        with ScopedSession() as local_db_session:
            config = local_db_session.query(ConfigModel).filter(
                ConfigModel.name == name).first()

            if name == TERMS_OF_SERVICE:
                # Use UpdateTermsOfService mutation instead.
                return SaveConfig(success=False)

            if config:
                config.value = value
            else:
                config = ConfigModel(name=name, value=value)
                local_db_session.add(config)

            return SaveConfig(success=True)


class SendEmail(graphene.Mutation):
    """Mutation to customise foyer."""
    success = graphene.Boolean(description="True if the config was saved.")

    class Arguments:
        subject = graphene.String(
            required=True, description="The subject of the email.")
        body = graphene.String(
            required=True, description="The body of the email. HTML is allowed.")
        recipients = graphene.String(
            required=True, description="The recipients of the email. Comma separated.")
        bcc = graphene.String(
            required=False, description="The bcc recipients of the email. Comma separated.")

    @jwt_required()
    def mutate(self, info, subject, body, recipients, bcc):
        code, error, user, timezone = current_user()
        if not user.role in (ADMIN, SUPER_ADMIN) and not user.can_send_email:
            raise Exception(
                "Only Admin can send notification emails!")

        send(recipients.split(','), subject, body, bcc.split(','))
        return SendEmail(success=True)


class Mutation(graphene.ObjectType):
    updateTermsOfService = UpdateTermsOfService.Field()
    saveConfig = SaveConfig.Field()
    sendEmail = SendEmail.Field()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
config_schema = graphene.Schema(query=Query, mutation=Mutation)
app.add_url_rule(
    f'/{URL_PREFIX}config_graphql/', view_func=GraphQLView.as_view(
        "config_graphql", schema=config_schema,
        graphiql=True
    )
)

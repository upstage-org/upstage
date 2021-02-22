# -*- coding: iso8859-15 -*-
from config.project_globals import (DBSession, Base, metadata, engine, get_scoped_session,
                                    app, api, ScopedSession)
from utils import graphql_utils
from flask_graphql import GraphQLView
from asset.models import Stage as StageModel
from config.settings import VERSION
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphene import relay
import graphene
import sys
import os

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, '..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)


class StageAttribute:
    name = graphene.String(description="Stage Name")
    description = graphene.String(description="Stage Description")
    owner_id = graphene.String(description="User ID of the owner")
    file_location = graphene.String(description="Unique File Location")

class Stage(SQLAlchemyObjectType):
    db_id = graphene.Int(description="Database ID")

    class Meta:
        model = StageModel
        model.db_id = model.id
        interfaces = (relay.Node,)


class CreateStageInput(graphene.InputObjectType, StageAttribute):
    """Arguments to create a stage."""
    pass


class CreateStage(graphene.Mutation):
    """Mutation to create a user."""
    stage = graphene.Field(
        lambda: Stage, description="Stage created by this mutation.")

    class Arguments:
        input = CreateStageInput(required=True)

    def mutate(self, info, input):
        data = graphql_utils.input_to_dictionary(input)

        stage = StageModel(**data)
        # Add validation for non-empty passwords, etc.
        local_db_session = get_scoped_session()
        local_db_session.add(stage)
        local_db_session.flush()
        stage_id = stage.id
        local_db_session.commit()

        stage = DBSession.query(StageModel).filter(
            StageModel.id == stage_id).first()
        return CreateStage(stage=stage)


class UpdateStageInput(graphene.InputObjectType, StageAttribute):
    """Arguments to update a user."""
    id = graphene.ID(required=True, description="Global Id of the stage.")


class UpdateStage(graphene.Mutation):
    """Update a user."""
    stage = graphene.Field(
        lambda: Stage, description="Stage updated by this mutation.")

    class Arguments:
        input = UpdateStageInput(required=True)

    # decorate this with jwt login decorator.
    def mutate(self, info, input):
        data = graphql_utils.input_to_dictionary(input)
        local_db_session = get_scoped_session()

        stage = local_db_session.query(StageModel)\
            .filter(StageModel.id == data['id']).first()
        for key, value in data.items():
            if hasattr(stage, key):
                setattr(stage, key, value)
        local_db_session.commit()
        stage = DBSession.query(StageModel).filter(
            StageModel.id == data['id']).first()

        return UpdateStage(stage=stage)


class Mutation(graphene.ObjectType):
    createStage = CreateStage.Field()
    updateStage = UpdateStage.Field()


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    stageList = SQLAlchemyConnectionField(Stage.connection)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
stage_schema = graphene.Schema(query=Query, mutation=Mutation)
app.add_url_rule(
    f'/{VERSION}/stage_graphql/', view_func=GraphQLView.as_view(
        "stage_graphql", schema=stage_schema,
        graphiql=True
    )
)

import os
import sys
import graphene
import json

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, ".."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from core.asset.models import (
    Asset as AssetModel,
    Stage as StageModel,
    StageAttribute as StageAttributeModel,
)
from core.user.models import User as UserModel
from flask_jwt_extended.view_decorators import verify_jwt_in_request
from flask_jwt_extended.utils import get_jwt_identity
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy.fields import SQLAlchemyConnectionField
from graphql_relay.node.node import from_global_id
from core.utils.graphql_utils import CountableConnection, input_to_dictionary


class Stage(SQLAlchemyObjectType):
    db_id = graphene.Int(description="Database ID")
    permission = graphene.String(description="Player access to this stage")

    class Meta:
        model = StageModel
        interfaces = (graphene.relay.Node,)
        connection_class = CountableConnection

    def resolve_db_id(self, info):
        return self.id

    def resolve_permission(self, info):
        result = verify_jwt_in_request(True)
        user_id = get_jwt_identity()
        if not user_id:
            return "audience"
        if self.owner_id == user_id:
            return "owner"
        player_access = self.attributes.filter(
            StageAttributeModel.name == "playerAccess"
        ).first()
        if player_access:
            accesses = json.loads(player_access.description)
            if len(accesses) == 2:
                if user_id in accesses[0]:
                    return "player"
                elif user_id in accesses[1]:
                    return "editor"
                return "audience"


class StageConnectionField(SQLAlchemyConnectionField):
    RELAY_ARGS = ["first", "last", "before", "after"]

    @classmethod
    def get_query(cls, model, info, sort=None, **args):
        query = super(StageConnectionField, cls).get_query(model, info, sort, **args)

        verify_jwt_in_request(True)
        for field, value in args.items():
            if field == "id":
                _type, _id = from_global_id(value)
                query = query.filter(getattr(model, field) == _id)
            elif field == "owners":
                if len(value):
                    query = query.filter(
                        getattr(model, "owner").has(UserModel.username.in_(value))
                    )
            elif field == "created_between":
                if len(value) == 2:
                    query = query.filter(AssetModel.created_on >= value[0]).filter(
                        AssetModel.created_on <= value[1]
                    )
            elif len(field) > 5 and field[-4:] == "like":
                query = query.filter(getattr(model, field[:-5]).ilike(f"%{value}%"))
            elif field not in cls.RELAY_ARGS and hasattr(model, field):
                query = query.filter(getattr(model, field) == value)
        return query

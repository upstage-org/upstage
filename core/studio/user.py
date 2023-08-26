import os
import sys
import graphene

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, ".."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from core.asset.models import (
    Asset as AssetModel,
)
from core.user.models import User as UserModel, role_conv
from flask_jwt_extended.view_decorators import verify_jwt_in_request
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy.fields import SQLAlchemyConnectionField
from graphql_relay.node.node import from_global_id
from core.utils.graphql_utils import CountableConnection


class AdminPlayer(SQLAlchemyObjectType):
    db_id = graphene.Int(description="Database ID")
    permission = graphene.String(description="Player access to this user")
    role_name = graphene.String(description="Name of the role")

    class Meta:
        model = UserModel
        interfaces = (graphene.relay.Node,)
        connection_class = CountableConnection

    def resolve_role_name(self, info):
        return role_conv(self.role)


class UserConnectionField(SQLAlchemyConnectionField):
    RELAY_ARGS = ["first", "last", "before", "after"]

    @classmethod
    def get_query(cls, model, info, sort=None, **args):
        query = super(UserConnectionField, cls).get_query(model, info, sort, **args)

        verify_jwt_in_request(True)
        for field, value in args.items():
            if field == "id":
                _type, _id = from_global_id(value)
                query = query.filter(getattr(model, field) == _id)
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

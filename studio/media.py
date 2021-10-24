import hashlib
import json
import os
import sys
import time
import uuid
from base64 import b64decode
from datetime import datetime, timedelta

import graphene
from asset.models import Asset as AssetModel, Stage as StageModel
from asset.models import AssetType as AssetTypeModel
from user.models import User as UserModel
from config.project_globals import ScopedSession, appdir
from config.settings import STREAM_EXPIRY_DAYS, STREAM_KEY
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_jwt_extended.view_decorators import verify_jwt_in_request
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy.fields import SQLAlchemyConnectionField
from graphql_relay.node.node import from_global_id
from licenses.models import AssetLicense
from performance_config.models import ParentStage
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import and_, or_
from user.models import ADMIN, SUPER_ADMIN
from user.user_utils import current_user
from utils.graphql_utils import CountableConnection, input_to_dictionary

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, '..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)


absolutePath = os.path.dirname(appdir)
storagePath = 'ui/static/assets'


class AssignedStage(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    url = graphene.String()


class Asset(SQLAlchemyObjectType):
    db_id = graphene.Int(description="Database ID")
    src = graphene.String(description="Logical path of the media")
    stages = graphene.List(
        AssignedStage, description="Stages that this media is assigned to")
    copyright_level = graphene.Int(description="Copyright level")
    playerAccess = graphene.String(
        description="Users who can access and edit this media")
    permission = graphene.String(
        description="What permission the logged in user is granted to this media")
    sign = graphene.String(
        description="Stream sign that is required to publish from broadcaster")

    class Meta:
        model = AssetModel
        model.db_id = model.id
        interfaces = (graphene.relay.Node,)
        connection_class = CountableConnection

    def resolve_src(self, info):
        timestamp = int(time.mktime(self.updated_on.timetuple()))
        return self.file_location + '?t=' + str(timestamp)

    def resolve_stages(self, info):
        return [{'id': x.stage_id, 'name': x.stage.name, 'url': x.stage.file_location} for x in self.stages.all()]

    def resolve_copyright_level(self, info):
        if self.asset_license:
            return self.asset_license.level
        return 0

    def resolve_playerAccess(self, info):
        if self.asset_license and self.asset_license.permissions:
            return self.asset_license.permissions
        return "[]"

    def resolve_permission(self, info):
        result = verify_jwt_in_request(True)
        user_id = get_jwt_identity()
        if not user_id:
            return "none"
        if self.owner_id == user_id:
            return 'owner'
        if not self.asset_license or self.asset_license.level == 0:
            return "editor"
        if self.asset_license.level == 3:
            return "none"
        player_access = self.asset_license.permissions
        if player_access:
            accesses = json.loads(player_access)
            if len(accesses) == 2:
                if user_id in accesses[0]:
                    return "readonly"
                elif user_id in accesses[1]:
                    return "editor"
        return "none"

    def resolve_sign(self, info):
        result = verify_jwt_in_request(True)
        user_id = get_jwt_identity()
        if self.owner_id == user_id:
            timestamp = int(
                (datetime.now() + timedelta(days=STREAM_EXPIRY_DAYS)).timestamp())
            payload = "/live/{0}-{1}-{2}".format(
                self.file_location, timestamp, STREAM_KEY)
            hashvalue = hashlib.md5(payload.encode('utf-8')).hexdigest()
            return "{0}-{1}".format(timestamp, hashvalue)
        return ''


class AssetType(SQLAlchemyObjectType):
    db_id = graphene.Int(description="Database ID")

    class Meta:
        model = AssetTypeModel
        model.db_id = model.id
        interfaces = (graphene.relay.Node,)


class AssetConnectionField(SQLAlchemyConnectionField):
    RELAY_ARGS = ['first', 'last', 'before', 'after']

    @classmethod
    def get_query(cls, model, info, sort=None, **args):
        query = super(AssetConnectionField, cls).get_query(
            model, info, sort, **args)

        result = verify_jwt_in_request(True)
        user_id = get_jwt_identity()
        query = query.filter(or_(
            AssetModel.asset_license == None,
            AssetModel.asset_license.has(AssetLicense.level < 3),
            and_(AssetModel.asset_license.has(AssetLicense.level == 3),
                 AssetModel.owner_id == user_id)
        ))
        for field, value in args.items():
            if field == 'id':
                _type, _id = from_global_id(value)
                query = query.filter(getattr(model, field) == _id)
            elif field == 'media_types':
                if len(value):
                    query = query.filter(getattr(model, 'asset_type').has(
                        AssetTypeModel.name.in_(value)))
            elif field == 'owners':
                if len(value):
                    query = query.filter(getattr(model, 'owner').has(
                        UserModel.username.in_(value)))
            elif field == 'stages':
                if len(value):
                    query = query\
                        .join(ParentStage, AssetModel.stages)\
                        .filter(ParentStage.stage_id.in_(value))
            elif field == 'created_between':
                if len(value) == 2:
                    query = query\
                        .filter(AssetModel.created_on >= value[0])\
                        .filter(AssetModel.created_on <= value[1])
            elif len(field) > 5 and field[-4:] == 'like':
                query = query.filter(
                    getattr(model, field[:-5]).ilike(f"%{value}%"))
            elif field not in cls.RELAY_ARGS and hasattr(model, field):
                query = query.filter(getattr(model, field) == value)
        return query


class CalcSizes(graphene.Mutation):
    """Mutation to assign stages to a media."""
    size = graphene.Int(description="Total calculated sizes")

    # decorate this with jwt login decorator.
    def mutate(self, info):
        total = 0
        with ScopedSession() as local_db_session:
            for media in local_db_session.query(AssetModel):
                if not media.size:
                    full_path = os.path.join(
                        absolutePath, storagePath, media.file_location)
                    try:
                        size = os.path.getsize(full_path)
                    except:
                        size = 0  # file not exist
                    media.size = size
                    local_db_session.flush()
                total += media.size

            local_db_session.commit()
            local_db_session.close()
            return CalcSizes(size=total)

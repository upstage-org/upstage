import hashlib
import json
from operator import itemgetter
import os
import sys
import time
import uuid
from base64 import b64decode
from datetime import datetime, timedelta

import graphene
from asset.models import Asset as AssetModel, MediaTag, Stage as StageModel, Tag
from asset.models import AssetType as AssetTypeModel
from user.models import PLAYER, User as UserModel
from config.project_globals import DBSession, ScopedSession, appdir
from config.settings import STREAM_EXPIRY_DAYS, STREAM_KEY
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_jwt_extended.view_decorators import verify_jwt_in_request
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy.fields import SQLAlchemyConnectionField
from graphql_relay.node.node import from_global_id
from licenses.models import AssetLicense, AssetUsage as AssetUsageModel
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


class AssetUsage(SQLAlchemyObjectType):
    class Meta:
        model = AssetUsageModel
        interfaces = (graphene.relay.Node,)


class Previlege(graphene.Enum):
    NONE = 0
    OWNER = 1
    APPROVED = 2
    PENDING_APPROVAL = 3
    REQUIRE_APPROVAL = 4


class Asset(SQLAlchemyObjectType):
    db_id = graphene.Int(description="Database ID")
    src = graphene.String(description="Logical path of the media")
    stages = graphene.List(
        AssignedStage, description="Stages that this media is assigned to")
    permissions = graphene.List(
        AssetUsage, description="Users who had been granted or acknowledged to use this media")
    privilege = Previlege(
        description="Permission of the logged in user for this media")
    sign = graphene.String(
        description="Stream sign that is required to publish from broadcaster")
    tags = graphene.List(graphene.String, description="Media tags")

    class Meta:
        model = AssetModel
        interfaces = (graphene.relay.Node,)
        connection_class = CountableConnection

    def resolve_db_id(self, info):
        return self.id

    def resolve_src(self, info):
        timestamp = int(time.mktime(self.updated_on.timetuple()))
        return self.file_location + '?t=' + str(timestamp)

    def resolve_stages(self, info):
        return [{'id': x.stage_id, 'name': x.stage.name, 'url': x.stage.file_location} for x in self.stages.all()]

    def resolve_tags(self, info):
        return [x.tag.name for x in self.tags.all()]

    def resolve_permissions(self, info):
        return self.permissions.order_by(AssetUsageModel.created_on.desc()).all()

    def resolve_privilege(self, info):
        result = verify_jwt_in_request(True)
        user_id = get_jwt_identity()
        if not user_id:
            return Previlege.NONE
        if self.owner_id == user_id:
            return Previlege.OWNER
        if not self.copyright_level:  # no copyright
            return Previlege.APPROVED
        if self.copyright_level == 3:
            # not shared, will not visisble to anyone either, this condidtion is just in case
            return Previlege.NONE
        usage = DBSession.query(AssetUsageModel).filter(
            AssetUsageModel.asset_id == self.id).filter(AssetUsageModel.user_id == user_id).first()
        if usage:
            if not usage.approved and self.copyright_level == 2:
                return Previlege.PENDING_APPROVAL
            else:
                return Previlege.APPROVED
        else:
            return Previlege.REQUIRE_APPROVAL

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
        interfaces = (graphene.relay.Node,)

    def resolve_db_id(self, info):
        return self.id


class AssetConnectionField(SQLAlchemyConnectionField):
    RELAY_ARGS = ['first', 'last', 'before', 'after']

    @classmethod
    def get_query(cls, model, info, sort=None, **args):
        query = super(AssetConnectionField, cls).get_query(
            model, info, sort, **args)

        result = verify_jwt_in_request(True)
        user_id = get_jwt_identity()
        query = query.filter(or_(
            AssetModel.copyright_level < 3,
            AssetModel.copyright_level == 3 and AssetModel.owner_id == user_id
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
            elif field == 'tags':
                if len(value):
                    query = query\
                        .join(MediaTag, AssetModel.tags)\
                        .join(Tag, MediaTag.tag)\
                        .filter(Tag.name.in_(value))
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

            return CalcSizes(size=total)


class UploadFile(graphene.Mutation):
    """Mutation to upload a media."""
    url = graphene.String(description="Uploaded file url")

    class Arguments:
        base64 = graphene.String(
            required=True, description="Base64 encoded content of the uploading media")
        filename = graphene.String(
            required=True, description="Original file name")

    @jwt_required()
    def mutate(self, info, base64, filename):
        code, error, user, timezone = current_user()
        if not user.role in (ADMIN, SUPER_ADMIN, PLAYER):
            raise Exception("You don't have permission to upload media")

        # Save base64 to file
        filename, file_extension = os.path.splitext(filename)
        unique_filename = uuid.uuid4().hex + file_extension
        subpath = 'media'
        mediaDirectory = os.path.join(
            absolutePath, storagePath, subpath)
        if not os.path.exists(mediaDirectory):
            os.makedirs(mediaDirectory)
        with open(os.path.join(mediaDirectory, unique_filename), "wb") as fh:
            fh.write(b64decode(base64.split(',')[1]))

        file_location = os.path.join(subpath, unique_filename)
        return UploadFile(url=file_location)


class SaveStageInput(graphene.InputObjectType):
    """Arguments to update a stage."""
    name = graphene.String(
        required=True, description="Name of the media")
    urls = graphene.List(
        graphene.String, description="Uploaded url of files")
    media_type = graphene.String(
        description="Avatar/prop/backdrop,... default to just a generic media", default_value='media')
    id = graphene.ID(description="ID of the media (for updating)")
    copyright_level = graphene.Int(description="Copyright level")
    user_ids = graphene.List(
        graphene.Int, description="Users who can access and edit this media")
    stage_ids = graphene.List(
        graphene.Int, description="Id of stages to be assigned to")
    tags = graphene.List(
        graphene.String, description="Media tags")
    w = graphene.Int(description="Width of the media")
    h = graphene.Int(description="Height of the media")


class SaveMedia(graphene.Mutation):
    """Mutation to upload a media."""
    asset = graphene.Field(
        lambda: Asset, description="Media saved by this mutation.")

    class Arguments:
        input = SaveStageInput(required=True)

    @jwt_required()
    def mutate(self, info, input):
        name, urls, media_type, copyright_level, user_ids, stage_ids, tags, w, h = itemgetter(
            'name', 'urls', 'media_type', 'copyright_level', 'user_ids', 'stage_ids', 'tags', 'w', 'h')(input)
        current_user_id = get_jwt_identity()
        with ScopedSession() as local_db_session:
            asset_type = local_db_session.query(AssetTypeModel).filter(
                AssetTypeModel.name == media_type).first()
            if not asset_type:
                asset_type = AssetTypeModel(
                    name=media_type, file_location=media_type)
                local_db_session.add(asset_type)
                local_db_session.flush()

            if 'id' in input:
                id = from_global_id(input['id'])[1]
                asset = local_db_session.query(AssetModel).filter(
                    AssetModel.id == id).first()
            else:
                asset = AssetModel(owner_id=current_user_id)
                local_db_session.add(asset)

            if asset:
                asset.name = name
                asset.asset_type = asset_type
                asset.file_location = urls[0]
                asset.copyright_level = copyright_level
                asset.updated_on = datetime.utcnow()
                local_db_session.flush()

            if urls:
                if not asset.description:
                    asset.description = "{}"
                attributes = json.loads(asset.description)
                if not 'frame' in attributes or attributes['frames']:
                    attributes['frames'] = []

                asset.size = 0
                for url in urls:
                    attributes['frames'].append(url)
                    full_path = os.path.join(absolutePath, storagePath, url)
                    try:
                        size = os.path.getsize(full_path)
                    except:
                        size = 0  # file not exist
                    asset.size += size

                if len(urls) > 1:
                    attributes['multi'] = True
                else:
                    attributes['multi'] = False
                    attributes['frames'] = []
                attributes['w'] = w
                attributes['h'] = h

                asset.description = json.dumps(attributes)
                local_db_session.flush()

            if stage_ids:
                asset.stages.delete()
                for id in stage_ids:
                    asset.stages.append(ParentStage(stage_id=id))

            if user_ids != None:
                granted_permissions = asset.permissions.all()
                for permission in granted_permissions:
                    if isinstance(permission, AssetUsageModel):
                        if permission.user_id not in user_ids and permission.approved == True:
                            asset.permissions.remove(permission)
                            local_db_session.delete(permission)
                for user_id in user_ids:
                    permission = local_db_session.query(AssetUsageModel).filter(
                        AssetUsageModel.asset_id == asset.id, AssetUsageModel.user_id == user_id).first()
                    if not permission:
                        permission = AssetUsageModel(user_id=user_id)
                        asset.permissions.append(permission)
                    permission.approved = True
                local_db_session.flush()

            if tags:
                asset.tags.delete()
                for tag in tags:
                    tag_model = local_db_session.query(
                        Tag).filter(Tag.name == tag).first()
                    if not tag_model:
                        tag_model = Tag(name=tag)
                        local_db_session.add(tag_model)
                        local_db_session.flush()
                    asset.tags.append(MediaTag(tag_id=tag_model.id))

            local_db_session.flush()
            local_db_session.commit()
            asset = local_db_session.query(AssetModel).filter(
                AssetModel.id == asset.id).first()
            return SaveMedia(asset=asset)


class ConfirmPermission(graphene.Mutation):
    """Mutation to approve or reject a media usage request"""
    success = graphene.Boolean(description="Success")
    message = graphene.String(description="Reason for why the mutation failed")
    permissions = graphene.List(
        lambda: AssetUsage, description="Permissions that were updated")

    class Arguments:
        id = graphene.ID(description="ID of the media usage request")
        approved = graphene.Boolean(
            description="Whether the permission is approved. True for approving, False for rejecting")

    @jwt_required()
    def mutate(self, info, id, approved):
        id = from_global_id(id)[1]
        with ScopedSession() as local_db_session:
            asset_usage = local_db_session.query(AssetUsageModel).get(id)
            asset_id = asset_usage.asset_id
            if asset_usage:
                code, error, user, timezone = current_user()
                if not user.role in (ADMIN, SUPER_ADMIN):
                    if not user.id == asset_usage.asset.owner_id:
                        return ConfirmPermission(success=False, message="Only media owner or admin can delete this media!")
                if approved:
                    asset_usage.approved = True
                    asset_usage.seen = True
                else:
                    local_db_session.delete(asset_usage)
                local_db_session.flush()
        permissions = DBSession.query(AssetUsageModel).filter(
            AssetUsageModel.asset_id == asset_id).all()
        return ConfirmPermission(success=True, permissions=permissions)


class RequestPermission(graphene.Mutation):
    """Mutation to create an asset usage"""
    success = graphene.Boolean(description="Success")

    class Arguments:
        asset_id = graphene.ID(description="ID of the media usage request")
        note = graphene.String(
            description="Note for the media usage request", required=False)

    @jwt_required()
    def mutate(self, info, asset_id, note=None):
        asset_id = from_global_id(asset_id)[1]
        with ScopedSession() as local_db_session:
            asset = local_db_session.query(AssetModel).get(asset_id)
            if asset:
                code, error, user, timezone = current_user()
                asset_usage = AssetUsageModel(
                    user_id=user.id, asset_id=asset_id, note=note)
                if asset.copyright_level == 2:
                    asset_usage.approved = False
                else:
                    asset_usage.approved = True
                local_db_session.add(asset_usage)
                local_db_session.flush()
                local_db_session.commit()
        return ConfirmPermission(success=True)

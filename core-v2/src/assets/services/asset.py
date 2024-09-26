from base64 import b64decode
from datetime import datetime, timedelta
import hashlib
import json
from operator import or_
import os
from typing import Optional
import uuid
import time

from assets.entities.asset import AssetEntity
from assets.entities.asset_license import AssetLicenseEntity
from assets.entities.asset_type import AssetTypeEntity
from assets.entities.asset_usage import AssetUsageEntity
from assets.entities.media_tag import MediaTagEntity
from assets.entities.tag import TagEntity
from assets.http.validation import MediaTableInput, SaveMediaInput
from config.database import DBSession, ScopedSession
from config.env import STREAM_EXPIRY_DAYS, STREAM_KEY
from core.helpers.object import convert_keys_to_camel_case
from stages.entities.parent_stage import ParentStageEntity
from users.entities.user import ADMIN, SUPER_ADMIN, UserEntity
from graphql import GraphQLError

appdir = os.path.abspath(os.path.dirname(__file__))
absolutePath = os.path.dirname(appdir)
storagePath = "../../uploads/assets"


class AssetService:
    def __init__(self):
        pass

    def get_all_medias(self, user: UserEntity, filter: dict = None):
        query = (
            DBSession.query(AssetEntity)
            .join(AssetTypeEntity)
            .join(UserEntity)
            .outerjoin(AssetLicenseEntity)
        )

        if "mediaType" in filter:
            query = query.filter(AssetTypeEntity.name == filter["mediaType"])

        if "owner" in filter:
            query = query.filter(UserEntity.username == filter["owner"])

        assets = query.all()

        return [self.resolve_fields(asset, user) for asset in assets]

    def search_assets(self, search_assets: MediaTableInput):
        total_count = DBSession.query(AssetEntity).count()

        query = DBSession.query(AssetEntity).outerjoin(AssetLicenseEntity)
        if search_assets.name:
            query = query.filter(AssetEntity.name.like(f"%{search_assets.name}%"))
        if search_assets.mediaTypes:
            query = query.join(AssetTypeEntity).filter(
                AssetTypeEntity.name.in_(search_assets.mediaTypes)
            )
        if search_assets.owners:
            query = query.join(UserEntity).filter(
                UserEntity.username.in_(search_assets.owners)
            )

        if search_assets.stages:
            query = query.filter(
                AssetEntity.stages.any(
                    ParentStageEntity.stage_id.in_(search_assets.stages)
                )
            )
        if search_assets.tags:
            query = (
                query.join(MediaTagEntity)
                .join(TagEntity)
                .filter(TagEntity.name.in_(search_assets.tags))
            )
        if search_assets.createdBetween:
            query = query.filter(
                AssetEntity.created_on.between(
                    search_assets.createdBetween[0], search_assets.createdBetween[1]
                )
            )

        if search_assets.sort:
            sort = search_assets.sort
            for sort_option in sort:
                field, direction = sort_option.rsplit("_", 1)
                if field == "ASSET_TYPE_ID":
                    sort_field = AssetEntity.asset_type_id
                elif field == "OWNER_ID":
                    sort_field = AssetEntity.owner_id
                elif field == "NAME":
                    sort_field = AssetEntity.name
                elif field == "CREATED_ON":
                    sort_field = AssetEntity.created_on

                if direction == "ASC":
                    query = query.order_by(sort_field.asc())
                elif direction == "DESC":
                    query = query.order_by(sort_field.desc())
        if search_assets.page and search_assets.limit:
            query = query.limit(search_assets.limit).offset(
                (search_assets.page - 1) * search_assets.limit
            )

        print("AAAAA")
        assets = query.all()
        return convert_keys_to_camel_case({"totalCount": total_count, "edges": assets})

    def upload_file(self, base64: str, filename: str):
        filename, file_extension = os.path.splitext(filename)
        unique_filename = uuid.uuid4().hex + file_extension
        subpath = "media"
        media_directory = os.path.join(absolutePath, storagePath, subpath)
        if not os.path.exists(media_directory):
            os.makedirs(media_directory)
        with open(os.path.join(media_directory, unique_filename), "wb") as fh:
            fh.write(b64decode(base64.split(",")[1]))

        file_location = os.path.join(subpath, unique_filename)
        return {"url": file_location}

    def save_media(self, owner: UserEntity, input: SaveMediaInput):
        asset = None
        with ScopedSession() as local_db_session:
            asset_type = self.validate_asset_type(input, local_db_session)

            if input.id:
                asset = (
                    local_db_session.query(AssetEntity)
                    .filter(AssetEntity.id == input.id)
                    .first()
                )
                if (
                    owner.role not in [SUPER_ADMIN, ADMIN]
                    and asset.owner_id != owner.id
                ):
                    raise GraphQLError("You are not allowed to update this asset")
            else:
                asset = AssetEntity(owner_id=owner.id)
                local_db_session.add(asset)

            asset.name = input.name
            asset.asset_type_id = asset_type.id
            asset.copyright_level = input.copyrightLevel
            file_location = self.process_file_location(input, local_db_session, asset)

            self.change_owner(owner, local_db_session, asset)

            self.process_urls(input, local_db_session, asset_type, asset, file_location)

            self.update_asset_permissions(input, local_db_session, asset)
            asset = self.update_asset_tags(input, local_db_session, asset)
            local_db_session.commit()
            local_db_session.flush()

            return convert_keys_to_camel_case({"asset": {"id": asset.id}})

    def update_asset_tags(
        self, input: SaveMediaInput, local_db_session, asset: AssetEntity
    ):
        if input.tags:
            tags = input.tags
            asset.tags.delete()
            for tag in tags:
                tag_model = (
                    local_db_session.query(TagEntity)
                    .filter(TagEntity.name == tag)
                    .first()
                )
                if not tag_model:
                    tag_model = TagEntity(name=tag)
                    local_db_session.add(tag_model)
                    local_db_session.flush()
                asset.tags.append(MediaTagEntity(tag_id=tag_model.id))

            local_db_session.flush()
            local_db_session.commit()
            asset = (
                local_db_session.query(AssetEntity)
                .filter(AssetEntity.id == asset.id)
                .first()
            )

        return asset

    def create_asset(
        self,
        owner: UserEntity,
        asset_type_id: int,
        name: str,
        file_location: str,
        local_db_session,
    ):
        asset = AssetEntity(
            owner_id=owner.id,
            asset_type_id=asset_type_id,
            name=name,
            file_location=file_location,
        )
        local_db_session.add(asset)
        local_db_session.commit()
        local_db_session.flush()
        local_db_session.refresh(asset)
        return asset

    def update_asset_permissions(
        self, input: SaveMediaInput, local_db_session, asset: AssetEntity
    ):
        if input.userIds:
            user_ids = input.userIds
            granted_permissions = asset.permissions.all()
            for permission in granted_permissions:
                if isinstance(permission, AssetUsageEntity):
                    if (
                        permission.user_id not in user_ids
                        and permission.approved == True
                    ):
                        asset.permissions.remove(permission)
                        local_db_session.delete(permission)
            for user_id in user_ids:
                permission = (
                    local_db_session.query(AssetUsageEntity)
                    .filter(
                        AssetUsageEntity.asset_id == asset.id,
                        AssetUsageEntity.user_id == user_id,
                    )
                    .first()
                )
                if not permission:
                    permission = AssetUsageEntity(user_id=user_id)
                    asset.permissions.append(permission)
                permission.approved = True
            local_db_session.flush()

    def process_urls(
        self,
        input: SaveMediaInput,
        local_db_session,
        asset_type: AssetTypeEntity,
        asset: AssetEntity,
        file_location: str,
    ):
        if input.urls:
            urls = input.urls
            if not asset.description:
                asset.description = "{}"

            attributes = json.loads(asset.description)

            if not "frames" in attributes or attributes["frames"]:
                attributes["frames"] = []

            asset.size = 0
            for url in urls:
                attributes["frames"].append(url)
                full_path = os.path.join(absolutePath, storagePath, url)
                try:
                    size = os.path.getsize(full_path)
                except:
                    size = 0  # file not exist
                asset.size += size

            attributes["multi"] = True if len(urls) > 0 else False
            attributes["frames"] = attributes["frames"] if len(urls) > 0 else []
            attributes["w"] = input.w
            attributes["h"] = input.h
            if asset_type.name == "stream" and "/" not in file_location:
                attributes["isRTMP"] = True

            if "voice" in input:
                voice = input["voice"]
                if voice and voice.voice:
                    attributes["voice"] = voice
                elif "voice" in attributes:
                    del attributes["voice"]

            if "link" in input:
                link = input["link"]
                if link and link.url:
                    attributes["link"] = link
                elif "link" in attributes:
                    del attributes["link"]

            attributes["note"] = input.note
            asset.description = json.dumps(attributes)
            local_db_session.flush()
        if input.stageIds != None:
            asset.stages = []
            for id in input.stageIds:
                asset.stages.append(ParentStageEntity(stage_id=id))

    def change_owner(self, owner: UserEntity, local_db_session, asset: AssetEntity):
        if owner:
            new_owner = (
                local_db_session.query(UserEntity)
                .filter(UserEntity.username == owner.username)
                .first()
            )
            if new_owner:
                if new_owner.id != asset.owner_id and owner.role in (
                    ADMIN,
                    SUPER_ADMIN,
                ):
                    asset.owner_id = new_owner.id
            else:
                raise GraphQLError("Owner not found")
        asset.updated_on = datetime.now()
        local_db_session.flush()

    def process_file_location(self, input, local_db_session, asset):
        file_location = input["urls"][0] if "urls" in input else input.urls[0]
        asset.file_location = uuid.uuid4()
        if "?" in file_location:
            file_location = file_location[: file_location.index("?")]
            if file_location != asset.file_location and "/" not in file_location:
                existed_asset = (
                    local_db_session.query(AssetEntity)
                    .filter(AssetEntity.file_location == file_location)
                    .filter(AssetEntity.id != asset.id)
                    .first()
                )
                if existed_asset:
                    raise GraphQLError(
                        "Stream with the same key already existed, please pick another unique key!"
                    )
            asset.file_location = file_location

        return file_location

    def validate_asset_type(self, input, local_db_session):
        media_type = input.mediaType
        asset_type = (
            local_db_session.query(AssetTypeEntity)
            .filter(AssetTypeEntity.name == media_type)
            .first()
        )

        if not asset_type:
            asset_type = AssetTypeEntity(name=media_type, file_location=media_type)
            local_db_session.add(asset_type)
            local_db_session.flush()

        return asset_type

    def delete_media(self, owner: UserEntity, id: int):
        with ScopedSession() as local_db_session:
            asset = (
                local_db_session.query(AssetEntity).filter(AssetEntity.id == id).first()
            )

            if not asset:
                raise GraphQLError("Media not found")

            if owner.role not in (ADMIN, SUPER_ADMIN) and owner.id != asset.owner_id:
                return {
                    "success": False,
                    "message": "Only media owner or admin can delete this media!",
                }

            self.cleanup_assets(local_db_session, asset)
            local_db_session.delete(asset)
            local_db_session.flush()
            local_db_session.commit()

            return {
                "success": True,
                "message": "Media deleted successfully!",
            }

    def cleanup_assets(self, local_db_session, asset: AssetEntity):
        if asset.description:
            attributes = json.loads(asset.description)
            print(attributes)
            if "frames" in attributes:
                for frame in attributes["frames"]:
                    frame_asset = (
                        local_db_session.query(AssetEntity)
                        .filter(
                            or_(
                                AssetEntity.file_location == frame,
                                AssetEntity.description.contains(frame),
                            )
                        )
                        .first()
                    )
                    if frame_asset:
                        physical_path = os.path.join(absolutePath, storagePath, frame)
                        if os.path.exists(physical_path):
                            os.remove(physical_path)

        physical_path = os.path.join(absolutePath, storagePath, asset.file_location)
        local_db_session.query(ParentStageEntity).filter(
            ParentStageEntity.child_asset_id == asset.id
        ).delete(synchronize_session=False)
        local_db_session.query(MediaTagEntity).filter(
            MediaTagEntity.asset_id == asset.id
        ).delete(synchronize_session=False)
        local_db_session.query(AssetLicenseEntity).filter(
            AssetLicenseEntity.asset_id == asset.id
        ).delete(synchronize_session=False)
        local_db_session.query(AssetUsageEntity).filter(
            AssetUsageEntity.asset_id == asset.id
        ).delete(synchronize_session=False)

        for multiframe_media in (
            local_db_session.query(AssetEntity)
            .filter(AssetEntity.description.like(f"%{asset.file_location}%"))
            .all()
        ):
            attributes = json.loads(multiframe_media.description)
            for i, frame in enumerate(attributes["frames"]):
                if "?" in frame:
                    attributes["frames"][i] = frame[: frame.index("?")]
            if asset.file_location in attributes["frames"]:
                attributes["frames"].remove(asset.file_location)
            multiframe_media.description = json.dumps(attributes)
            local_db_session.flush()

        if os.path.exists(physical_path):
            os.remove(physical_path)

    def resolve_sign(self, user: UserEntity, asset: AssetEntity):
        if asset.owner_id == user.id:
            timestamp = int(
                (datetime.now() + timedelta(days=STREAM_EXPIRY_DAYS)).timestamp()
            )
            payload = "/live/{0}-{1}-{2}".format(
                asset.file_location, timestamp, STREAM_KEY
            )
            hashvalue = hashlib.md5(payload.encode("utf-8")).hexdigest()
            return "{0}-{1}".format(timestamp, hashvalue)
        return ""

    def resolve_src(self, asset: AssetEntity):
        timestamp = int(time.mktime(asset.updated_on.timetuple()))
        return asset.file_location + "?t=" + str(timestamp)

    def resolve_permissions(self, user_id: int, asset: AssetEntity):
        if not user_id:
            return "none"
        if asset.owner_id == user_id:
            return "owner"
        if not asset.asset_license or asset.asset_license.level == 0:
            return "editor"
        if asset.asset_license.level == 3:
            return "none"

        player_access = asset.asset_license.permissions if asset.asset_license else None
        if player_access:
            accesses = json.loads(player_access)
            if len(accesses) == 2:
                if user_id in accesses[0]:
                    return "readonly"
                elif user_id in accesses[1]:
                    return "editor"
        return "none"

    def resolve_fields(self, asset: AssetEntity, user: Optional[UserEntity] = None):
        src = self.resolve_src(asset)
        sign = self.resolve_sign(asset.owner, asset)
        user_id = user.id if user else asset.owner_id
        permission = self.resolve_permissions(user_id, asset)
        return {
            **convert_keys_to_camel_case(asset.to_dict()),
            "src": src,
            "sign": sign,
            "permission": permission,
        }
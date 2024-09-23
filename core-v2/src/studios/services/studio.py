from datetime import datetime
import os
from typing import List

from sqlalchemy import and_, asc, desc, or_
from assets.entities.asset import AssetEntity
from assets.entities.asset_usage import AssetUsageEntity
from authentication.entities.user_session import UserSessionEntity
from config.database import DBSession, ScopedSession
from config.env import UPSTAGE_FRONTEND_URL
from core.helpers.fernet_crypto import decrypt, encrypt
from core.helpers.object import convert_keys_to_camel_case
from mails.helpers.mail import send
from mails.templates.templates import (
    display_user,
    permission_response_for_media,
    request_permission_acknowledgement,
    request_permission_for_media,
    user_approved,
    waiting_request_media_approve,
)
from performance_config.entities.performance import PerformanceEntity
from stages.entities.parent_stage import ParentStageEntity
from stages.entities.stage import StageEntity
from stages.entities.stage_attribute import StageAttributeEntity
from studios.http.validation import BatchUserInput, ChangePasswordInput, UpdateUserInput
from users.entities.user import ADMIN, GUEST, SUPER_ADMIN, UserEntity
from graphql import GraphQLError

appdir = os.path.abspath(os.path.dirname(__file__))
absolutePath = os.path.dirname(appdir)
storagePath = "../../uploads/assets"


class StudioService:
    def __init__(self):
        pass

    def admin_players(self, params):
        totalCount = DBSession.query(UserEntity).count()
        query = DBSession.query(UserEntity)

        if "usernameLike" in params:
            query = query.filter(
                UserEntity.username.ilike(f"%{params['usernameLike']}%")
            )

        if "createdBetween" in params:
            start_date = datetime.strptime(params["createdBetween"][0], "%Y-%m-%d")
            end_date = datetime.strptime(params["createdBetween"][1], "%Y-%m-%d")
            query = query.filter(UserEntity.created_on.between(start_date, end_date))

        if "sort" in params:
            for sort_param in params["sort"]:
                if sort_param == "USERNAME_ASC":
                    query = query.order_by(asc(UserEntity.username))
                elif sort_param == "USERNAME_DESC":
                    query = query.order_by(desc(UserEntity.username))
                elif sort_param == "CREATED_ON_ASC":
                    query = query.order_by(asc(UserEntity.created_on))
                elif sort_param == "CREATED_ON_DESC":
                    query = query.order_by(desc(UserEntity.created_on))

        if "first" in params:
            limit = params["first"] or 10
            page = 0 if "page" not in params else (params["page"] - 1)
            offset = page * limit
            query = query.limit(limit).offset(offset)

        results = query.all()

        return convert_keys_to_camel_case(
            {"totalCount": totalCount, "edges": [user.to_dict() for user in results]}
        )

    def create_users(self, users: List[BatchUserInput]):
        with ScopedSession() as session:
            self.validate_user_information(users, session)

            for user in users:
                user = UserEntity(
                    username=user["username"],
                    email=user["email"],
                    active=True,
                    role=GUEST,
                    password=encrypt(user["password"]),
                )
                session.add(user)
            session.commit()

        users = (
            DBSession.query(UserEntity)
            .filter(UserEntity.email.in_([user["email"] for user in users]))
            .all()
        )
        return convert_keys_to_camel_case({"users": [user.to_dict() for user in users]})

    def validate_user_information(self, users: List[BatchUserInput], session):
        for user in users:
            BatchUserInput(**user)

        duplicated = []
        for i in range(len(users) - 1):
            for j in range(i + 1, len(users)):
                if (
                    users[i]["username"] == users[j]["username"]
                    or users[i]["email"] == users[j]["email"]
                ):
                    duplicated.append(users[i]["username"])

        if duplicated:
            raise GraphQLError(f"Duplicated user information {''.join(duplicated)}")

        existing_users = (
            session.query(UserEntity)
            .filter(
                or_(
                    UserEntity.username.in_([user["username"] for user in users]),
                    UserEntity.email.in_([user["email"] for user in users]),
                )
            )
            .all()
        )

        if existing_users:
            raise GraphQLError(
                f"Users with emails {', '.join([user.email for user in existing_users])} already exist"
            )

    async def update_user(self, input: UpdateUserInput):
        with ScopedSession() as session:
            try:
                self._validate_email(input)
                user = self._get_user(session, input.id)
                self._check_existing_email(input)
                self._update_user_fields(user, input)
                session.commit()
                session.flush()
            except Exception as e:
                raise GraphQLError(
                    f"There was an error updating this user information: {str(e)}. Please check the logs and try again later!"
                )

    def _validate_email(self, input: UpdateUserInput):
        if not input.email and input.role != GUEST:
            raise GraphQLError("Email is required!")

    def _get_user(self, session, user_id):
        user = session.query(UserEntity).filter(UserEntity.id == user_id).first()
        if not user:
            raise GraphQLError("User not found!")
        return user

    def _check_existing_email(self, input: UpdateUserInput):
        existing_email = (
            DBSession.query(UserEntity)
            .filter(and_(UserEntity.email == input.email, UserEntity.id != input.id))
            .first()
        )
        if existing_email:
            raise GraphQLError("This email address already belongs to another user!")

    async def _update_user_fields(self, user, input: UpdateUserInput):
        if input.password:
            user.password = encrypt(input.password)
        else:
            del input.password
        for key, value in input.items():
            if key == "active":
                await self._handle_active_status(user, value)
            if hasattr(user, key):
                setattr(user, key, value)

    async def _handle_active_status(self, user: UserEntity, value):
        if value and not user.active and not user.deactivated_on:
            await send(
                [user.email],
                f"Registration approved for user {user.username}",
                user_approved(user),
            )
        if not value and user.active:
            user.deactivated_on = datetime.now()

    def delete_user(self, id: int, current_user: UserEntity):
        with ScopedSession() as local_db_session:
            user = (
                local_db_session.query(UserEntity).filter(UserEntity.id == id).first()
            )
            if not user:
                raise GraphQLError("User not found!")

            local_db_session.query(UserSessionEntity).filter(
                UserSessionEntity.user_id == id
            ).delete()

            local_db_session.query(StageAttributeEntity).filter(
                StageAttributeEntity.stage.has(StageEntity.owner_id == id)
            ).delete(synchronize_session="fetch")

            local_db_session.query(ParentStageEntity).filter(
                ParentStageEntity.stage.has(StageEntity.owner_id == id)
            ).delete(synchronize_session="fetch")

            local_db_session.query(PerformanceEntity).filter(
                PerformanceEntity.stage.has(StageEntity.owner_id == id)
            ).delete(synchronize_session="fetch")

            local_db_session.query(StageEntity).filter(
                StageEntity.owner_id == id
            ).delete()
            local_db_session.query(AssetEntity).filter(
                AssetEntity.owner_id == id
            ).update({AssetEntity.owner_id: current_user.id})

            local_db_session.delete(user)
            local_db_session.commit()
            return convert_keys_to_camel_case(
                {"success": True, "message": "User deleted successfully!"}
            )

    def change_password(self, input: ChangePasswordInput):
        with ScopedSession() as local_db_session:
            user = (
                local_db_session.query(UserEntity)
                .filter(UserEntity.id == input.id)
                .first()
            )
            if not user:
                raise GraphQLError("User not found!")

            if decrypt(user.password) != input.oldPassword:
                raise GraphQLError("Old password is incorrect!")

            user.password = encrypt(input.newPassword)
            local_db_session.commit()
            local_db_session.flush()
            return convert_keys_to_camel_case(
                {"success": True, "message": "Password changed successfully!"}
            )

    def calc_sizes(self):
        with ScopedSession() as local_db_session:
            size = 0
            for media in local_db_session.query(AssetEntity).all():
                if not media.size:
                    full_path = os.path.join(
                        absolutePath, storagePath, media.file_location
                    )
                    try:
                        size = os.path.getsize(full_path)
                    except:
                        size = 0  # file not exist
                    media.size = size
                    local_db_session.flush()
                size += media.size

        return {"size": size}

    async def request_permission(self, user: UserEntity, asset_id: int, note: str):
        with ScopedSession() as local_db_session:
            asset = (
                local_db_session.query(AssetEntity)
                .filter(AssetEntity.id == asset_id)
                .first()
            )
            if not asset:
                raise GraphQLError("Asset not found!")
            asset_usage = AssetUsageEntity(
                user_id=user.id,
                asset_id=asset_id,
                note=note,
                approved=False,
                seen=False,
            )

            if asset.copyright_level == 2:
                asset_usage.approved = False
                studio_url = f"{UPSTAGE_FRONTEND_URL}stages"
                await send(
                    [asset.owner.email],
                    f"Pending permission request for media {asset.name}",
                    request_permission_for_media(user, asset, note, studio_url),
                )
                await send(
                    user.email,
                    f"Waiting permission request approval/denial for media {asset.name}",
                    waiting_request_media_approve(user, asset),
                )
            else:
                asset_usage.approved = True
                await send(
                    user.email,
                    f"{display_user(user)} was approved to use media: {asset.name}",
                    request_permission_acknowledgement(user, asset, note),
                )
            local_db_session.add(asset_usage)
            local_db_session.commit()
            local_db_session.flush()
            studio_url = f"{UPSTAGE_FRONTEND_URL}/stages"
            await send(
                [asset.owner.email],
                f"Permission requested for media {asset.name}",
                permission_response_for_media(user, asset, note, False, studio_url),
            )
        return {"success": True}

    async def confirm_permission(self, user: UserEntity, id: int, approved: bool):
        with ScopedSession() as local_db_session:
            asset_usage = (
                local_db_session.query(AssetUsageEntity)
                .filter(AssetUsageEntity.id == id)
                .first()
            )
            if not asset_usage:
                raise GraphQLError("Asset not found!")
            if (
                user.role not in [SUPER_ADMIN, ADMIN]
                and user.id != asset_usage.owner_id
            ):
                raise GraphQLError("You are not authorized to perform this action!")

            if approved:
                asset_usage.approved = True
                asset_usage.seen = True
                asset_usage.approved_on = datetime.now()
            else:
                local_db_session.delete(asset_usage)

            local_db_session.commit()
            local_db_session.flush()
            studio_url = f"{UPSTAGE_FRONTEND_URL}/stages"
            await send(
                [asset_usage.user.email],
                f"Permission approved for media {asset_usage.asset.name}"
                if approved
                else f"Permission rejected for media {asset_usage.asset.name}",
                permission_response_for_media(
                    asset_usage.user,
                    asset_usage.asset,
                    asset_usage.note,
                    approved,
                    studio_url,
                ),
            )
        permissions = (
            DBSession.query(AssetUsageEntity)
            .filter(AssetUsageEntity.asset_id == asset_usage.asset_id)
            .all()
        )
        return convert_keys_to_camel_case(
            {
                "permissions": [permission.to_dict() for permission in permissions],
                "success": True,
            },
        )

    def quick_assign_mutation(self, user: UserEntity, stage_id: int, asset_id: int):
        with ScopedSession() as local_db_session:
            asset = (
                local_db_session.query(AssetEntity)
                .filter(AssetEntity.id == asset_id)
                .first()
            )
            if not asset:
                raise GraphQLError("Asset not found!")

            stage = (
                local_db_session.query(StageEntity)
                .filter(StageEntity.id == stage_id)
                .first()
            )
            if not stage:
                raise GraphQLError("Stage not found!")

            asset.stages.append(
                ParentStageEntity(stage_id=stage_id, child_asset_id=asset_id)
            )
            local_db_session.commit()
            local_db_session.flush()
        return {"success": True}

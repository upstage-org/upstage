import os
import uuid
from config.project_globals import appdir, ScopedSession
from asset.models import Asset as AssetModel, AssetType as AssetTypeModel
from graphene_sqlalchemy import SQLAlchemyObjectType
import graphene
from base64 import b64decode
from config.settings import VERSION

storagePath = f'{VERSION}/static/'


class Asset(SQLAlchemyObjectType):
    db_id = graphene.Int(description="Database ID")

    class Meta:
        model = AssetModel
        model.db_id = model.id
        interfaces = (graphene.relay.Node,)


class UploadMedia(graphene.Mutation):
    """Mutation to upload a media."""
    asset = graphene.Field(
        lambda: Asset, description="Media uploaded by this mutation.")

    class Arguments:
        name = graphene.String(
            required=True, description="Name of the media")
        base64 = graphene.String(
            required=True, description="Base64 encoded content of the uploading media")
        media_type = graphene.String(
            description="Avatar/prop/backdrop,... default to just a generic media", default_value='media')

    def mutate(self, info, name, base64, media_type):
        # current_user_id = get_jwt_identity()
        absolutePath = os.path.dirname(appdir)

        with ScopedSession() as local_db_session:
            asset_type = local_db_session.query(AssetTypeModel).filter(
                AssetTypeModel.name == media_type).first()
            if not asset_type:
                asset_type = AssetTypeModel(
                    name=media_type, file_location=media_type)
                local_db_session.add(asset_type)
                local_db_session.flush()

            # Save base64 to file
            mediaDirectory = os.path.join(
                absolutePath, storagePath, media_type)
            if not os.path.exists(mediaDirectory):
                os.makedirs(mediaDirectory)
            file_location = os.path.join(
                storagePath, media_type, uuid.uuid4().hex)
            filename = os.path.join(absolutePath, file_location)
            with open(filename, "wb") as fh:
                fh.write(b64decode(base64))

            asset = AssetModel(
                name=name,
                file_location=file_location,
                asset_type_id=asset_type.id,
                owner_id=26)
            local_db_session.add(asset)
            local_db_session.flush()
            local_db_session.commit()
            asset = local_db_session.query(AssetModel).filter(
                AssetModel.id == asset.id).first()
            return UploadMedia(asset=asset)

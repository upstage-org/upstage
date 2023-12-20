from flask_jwt_extended.view_decorators import jwt_required
import graphene
from graphene_sqlalchemy.types import SQLAlchemyObjectType
import graphene
from config.project_globals import DBSession
from studio.media import AssetUsage
from user.user_utils import current_user
from licenses.models import AssetUsage as AssetUsageModel


class NotificationType(graphene.Enum):
    MEDIA_USAGE = 1


class Notification(graphene.ObjectType):
    type = NotificationType(description="Type of notification")
    mediaUsage = graphene.Field(
        AssetUsage, description="If notification is of type media usage, this object contain the permission request")

    class Meta:
        interfaces = (graphene.relay.Node,)

    def resolve_mediaUsage(self, info):
        return self.mediaUsage


@jwt_required()
def resolve_notifications(self, info):
    code, error, user, timezone = current_user()
    notifications = []
    if user:
        mediaUsages = [Notification(type=NotificationType.MEDIA_USAGE, mediaUsage=x)
                       for x in DBSession.query(AssetUsageModel).filter(AssetUsageModel.approved == False).filter(AssetUsageModel.asset.has(owner_id=user.id)).all()]
        notifications += mediaUsages
    return notifications

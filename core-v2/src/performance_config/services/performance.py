from graphql import GraphQLError
from config.database import ScopedSession
from event_archive.entities.event import EventEntity
from performance_config.entities.performance import PerformanceEntity
from stages.http.validation import PerformanceInput
from users.entities.user import UserEntity


class PerformanceService:
    def __init__(self):
        pass

    def update_performance(self, user: UserEntity, input: PerformanceInput):
        with ScopedSession() as local_db_session:
            performance = local_db_session.query(PerformanceEntity).filter_by(id=input.id).first()
            if not performance:
                raise GraphQLError("Performance not found")
            
            if user.role not in ["SUPER_ADMIN", "ADMIN"] and user.id != performance.owner_id:
                raise GraphQLError("You are not allowed to update this performance")

            performance.name = input.name
            performance.description = input.description
            local_db_session.flush()
            local_db_session.commit()
            return { "success": True }
        

    def delete_performance(self, user: UserEntity, id: int):
        with ScopedSession() as local_db_session:
            performance = local_db_session.query(PerformanceEntity).filter_by(id=id).first()
            if not performance:
                raise GraphQLError("Performance not found")
            
            if user.role not in ["SUPER_ADMIN", "ADMIN"] and user.id != performance.owner_id:
                raise GraphQLError("You are not allowed to delete this performance")

            local_db_session.query(EventEntity).filter(EventEntity.performance_id == id).delete(
                    synchronize_session=False
                )
            local_db_session.delete(performance)
            local_db_session.commit()
            return { "success": True }
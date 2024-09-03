from config.database import DBSession, ScopedSession
from users.entities.user import UserEntity


class UserService:
    def find_one(self, username: str, email: str):
        return (
            DBSession.query(UserEntity)
            .filter(or_(UserEntity.username == username, UserEntity.email == email))
            .first()
        )

    def find_by_id(self, user_id: int):
        return (
            DBSession.query(UserEntity)
            .filter(UserEntity.id == user_id, UserEntity.active.is_(True))
            .first()
        )

    def update(self, user: UserEntity):
        return DBSession.merge(user)

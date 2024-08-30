
import os
import sys

# Always on top
app_dir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(app_dir, "../.."))

if app_dir not in sys.path:
    sys.path.append(app_dir)
    sys.path.append(projdir)

from config.database import get_scoped_session
from core.helpers.fernet_crypto import encrypt
from users.entities.user import UserEntity



def create_some_users():
    db_session = get_scoped_session()
    for i in range(1,2):
        user = UserEntity(
            username=f"quang{i}",
            password=encrypt(f"Secret@123{i}"),
            email=f"quang{i}@no.none",
            active=True,
            role=32,
        )
        db_session.add(user)
    db_session.commit()
    db_session.close()


def modify_user():
    db_session = get_scoped_session()
    user = db_session.query(UserEntity).filter(UserEntity.username == "gloria2").one()
    user.password = encrypt('')
    #user.email = ("",)
    db_session.commit()


if __name__ == "__main__":
    create_some_users()
    #modify_user()
    # pass

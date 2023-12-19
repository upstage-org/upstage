from config.settings import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_POOL_SIZE
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(SQLALCHEMY_DATABASE_URI,
                       pool_size=SQLALCHEMY_POOL_SIZE, isolation_level="AUTOCOMMIT")
DBSession = scoped_session(sessionmaker(
    autocommit=True, autoflush=True, bind=engine))


def get_scoped_session() -> scoped_session:
    session = scoped_session(sessionmaker(
        autocommit=True, autoflush=True, bind=engine))
    session.begin()
    return session

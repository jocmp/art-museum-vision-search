from contextlib import contextmanager
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DB_URL = os.environ.get("DATABASE_URL")


@contextmanager
def db_session():
    """ Creates a context with an open SQLAlchemy session.
    """
    engine = create_engine(DB_URL)
    connection = engine.connect()
    db_session = scoped_session(sessionmaker(autoflush=True, bind=engine))
    yield db_session
    db_session.commit()
    db_session.close()
    connection.close()

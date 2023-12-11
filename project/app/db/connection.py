from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from decouple import config


def get_connection_string():
    """
    Creates the connection string using env variables

    Returns:
        str: connection string
    """
    USER = config("MYSQL_USER")
    PASSWORD = config("MYSQL_PASSWORD")
    HOST = config("MYSQL_HOST")
    PORT = config("MYSQL_PORT")
    DB = config("MYSQL_DB")
    conn = f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
    return conn


def engine_maker():
    """
    Creates the engine to connect to the DB

    Returns:
        Engine: connection engine
    """
    connection_string = get_connection_string()
    engine = create_engine(connection_string)
    return engine


engine = engine_maker()
SessionLocal = sessionmaker(bind=engine)


def get_session():
    """
    Creates a session to communicate to the DB.

    Yields:
        Session: an instance of Session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
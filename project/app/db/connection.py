from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from decouple import config


def get_connection_string():
    USER = config("MYSQL_USER")
    PASSWORD = config("MYSQL_PASSWORD")
    HOST = config("MYSQL_HOST")
    PORT = config("MYSQL_PORT")
    DB = config("MYSQL_DB")
    conn = f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
    return conn


def engine_maker():
    connection_string = get_connection_string()
    engine = create_engine(connection_string)
    return engine


engine = engine_maker()
SessionLocal = sessionmaker(bind=engine)
SessionTest = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_session_test():
    db = SessionTest()
    try:
        yield db
    finally:
        db.close()

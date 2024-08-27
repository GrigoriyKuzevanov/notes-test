from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config import settings


DB_PORT = settings.db_port
DB_HOST = settings.db_host
DB_USER = settings.db_user
DB_PASSWORD = settings.db_password
DB_NAME = settings.db_name


# SQLALCHEMY_DATABASE_URL = f"postgresql://fastapi_user:secret@postgres:5432/fastapi_db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

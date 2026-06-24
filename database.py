from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DB_URL, DB_URL_TEST

engine = create_engine(DB_URL)
test_engine = create_engine(DB_URL_TEST)

sessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = sessionLocal()

    try:
        yield db
    finally:
        db.close()
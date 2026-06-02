from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

url = "postgresql+psycopg://sushank:0102030405@localhost:5432/aicpapp"
engine = create_engine(url)
sessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()


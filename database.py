from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv(".env")
url = os.getenv("DB_URL")

engine = create_engine(url)
sessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()


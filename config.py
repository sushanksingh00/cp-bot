from dotenv import load_dotenv
import os

load_dotenv(".env")
DB_URL = os.getenv("DB_URL")

if not DB_URL:
    raise ValueError("DB_URL environment variable is missing")

DB_URL_TEST = os.getenv("DB_URL_TEST")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_URL = os.getenv("REDIS_URL")
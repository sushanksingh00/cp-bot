from dotenv import load_dotenv
import os

load_dotenv(".env")
DB_URL = os.getenv("DB_URL")
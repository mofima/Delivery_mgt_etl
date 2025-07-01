from dotenv import load_dotenv
import os

load_dotenv()

# Google Sheets
GOOGLE_SERVICE_ACCOUNT_PATH = os.getenv("GOOGLE_SERVICE_ACCOUNT_PATH")

# PostgreSQL
PG_HOST = os.getenv("PG_HOST")
PG_PORT = int(os.getenv("PG_PORT"))
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DATABASE = os.getenv("PG_DATABASE")
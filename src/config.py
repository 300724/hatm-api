import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_PORT = os.getenv("DB_PORT")

DATABASE_URL = (
    f"postgresql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
)

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

LOGS_DIRECTORY = "logs"


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
REFRESH_TOKEN_EXPIRE_IN_MINUTES = 60 * 24 * 7

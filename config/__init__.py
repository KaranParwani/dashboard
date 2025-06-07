import os

from dotenv import load_dotenv
import redis.asyncio as aioredis

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Load the .env file
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

HOST = os.getenv("APP_HOST")
PORT = os.getenv("APP_PORT")

SUPER_ADMIN_EMAIL = os.getenv("SUPER_ADMIN_EMAIL")
SUPER_ADMIN_PASSWORD = os.getenv("SUPER_ADMIN_PASSWORD")

SALT = os.getenv("SALT")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRY = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRY = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")

OPENAI_API_KEY = os.getenv("OPEN_AI_KEY")

ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS")

# Initialize Redis connection
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_DB = os.getenv("REDIS_DB")

try:
    REDIS_PORT = int(REDIS_PORT)
except (TypeError, ValueError):
    raise ValueError(f"Invalid REDIS_PORT value: {REDIS_PORT}. Ensure it's an integer.")

REDIS = aioredis.from_url(
    f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}", decode_responses=True
)

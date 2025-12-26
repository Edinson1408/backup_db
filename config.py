import os
from dotenv import load_dotenv

load_dotenv()

DB_ENGINE = os.getenv("DB_ENGINE")  # mysql | postgres | oracle | sqlserver

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "name": os.getenv("DB_NAME"),
}

R2_CONFIG = {
    "bucket": os.getenv("R2_BUCKET"),
    "access_key": os.getenv("R2_ACCESS_KEY"),
    "secret_key": os.getenv("R2_SECRET_KEY"),
    "endpoint": os.getenv("R2_ENDPOINT"),
}

# env.config.py
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

ENV_TYPE = os.getenv("ENV_TYPE")

DATABASE_CONNECT = os.getenv("DATABASE_CONNECT")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "Secret@123")
ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_MINUTES = os.getenv("JWT_ACCESS_TOKEN_MINUTES", "15")
JWT_REFRESH_TOKEN_DAYS = os.getenv("JWT_REFRESH_TOKEN_DAYS", "30")


# Apple
APPLE_ACCESS_TOKEN_CREATE = os.getenv("APPLE_ACCESS_TOKEN_CREATE")
APPLE_APP_ID = os.getenv("APPLE_APP_ID")
APPLE_APP_SECRET = os.getenv("APPLE_APP_SECRET")
APPLE_TEAM_ID = os.getenv("APPLE_TEAM_ID")

DATABASE_URL = f"{DATABASE_CONNECT}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
print(DATABASE_URL)

JWT_HEADER_NAME = "X-Access-Token"

CIPHER_KEY = os.getenv("CIPHER_KEY", b"DDVf4r4bxTZYJSfYJDNDx2i5_Lhjo1L1uA_Ya20fIWc=")
CLOUDFLARE_CAPTCHA_SECRETKEY = os.getenv("CLOUDFLARE_CAPTCHA_SECRETKEY")
CLOUDFLARE_CAPTCHA_VERIFY_ENDPOINT = os.getenv("CLOUDFLARE_CAPTCHA_VERIFY_ENDPOINT")


HOSTNAME = os.getenv("HOSTNAME")
ACCEPT_EMAIL_HOST = os.getenv("ACCEPT_EMAIL_HOST", "").split(",")
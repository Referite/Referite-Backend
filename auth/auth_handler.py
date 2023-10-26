import time
from typing import Dict
import bcrypt

import jwt
from decouple import config

from db import referee_id_connection
from models import RefereeIdBody


JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM", default="HS256")
COOKIE_NAME = config("COOKIE_NAME", default="access_token")


def token_response(token: str):
    return {
        "access_token": token
    }


def create_access_token(user_id: str) -> Dict[str, str]:
    """Return a JWT token for the user_id that expires in 1 hour"""
    payload = {
        "user_id": user_id,
        "expires": time.time() + 3600
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def get_decodeJWT(token: str) -> dict:
    """Return the decoded token if the token is valid, else return an empty dict"""
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}


async def check_user(id_body: RefereeIdBody):
    """Check if user exists in database return boolean"""
    user = referee_id_connection.find_one({"username": str(id_body.username)})
    return user is not None


async def check_password(id_body: RefereeIdBody):
    """Check if password is correct return boolean"""
    password = referee_id_connection.find_one({"username": str(id_body.username)})
    return bool(bcrypt.checkpw(id_body.password.encode("utf-8"), password['password'].encode("utf-8")))
    # return password is not None


def hash_password(id_body: RefereeIdBody):
    """Hash password"""
    return bcrypt.hashpw(id_body.password.encode("utf-8"), bcrypt.gensalt())

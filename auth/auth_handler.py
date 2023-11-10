from datetime import datetime, timedelta
from typing import Dict

import bcrypt
import jwt
from decouple import config
from fastapi import HTTPException, Request

from db import referee_id_connection, audience_connection
from models import RefereeIdBody

JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM", default="HS256")


def create_access_token(user_id: str) -> Dict[str, str]:
    """Return a JWT token for the user_id that expires in 1 day"""
    payload = {"user_id": user_id, "expires": (datetime.now() + timedelta(days=1)).isoformat()}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def get_decodeJWT(token: str) -> dict:
    """Return the decoded token if the token is valid, else return an empty dict"""
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except Exception:
        raise HTTPException(401, "Invalid credentials")
    if datetime.fromisoformat(decoded_token["expires"]) >= datetime.now():
        return decoded_token


def check_user(id_body: RefereeIdBody):
    """Check if user exists in database return boolean"""
    user = referee_id_connection.find_one({"username": str(id_body.username)})
    return user is not None


def check_password(id_body: RefereeIdBody):
    """Check if password is correct return boolean"""
    password = referee_id_connection.find_one({"username": str(id_body.username)})
    return bool(
        bcrypt.checkpw(
            id_body.password.encode("utf-8"), password["password"].encode("utf-8")
        )
    )



def hash_password(id_body: RefereeIdBody):
    """Hash password"""
    return bcrypt.hashpw(id_body.password.encode("utf-8"), bcrypt.gensalt())


def check_token(request: Request):
    try:
        req = request.headers["authorization"]
        if audience_connection.find_one({"audience_token": req}):
            return {"message": "Authorize"}
        payload = get_decodeJWT(req)
        user = referee_id_connection.find_one(
            {"username": payload.get("user_id")}, {"_id": 0}
        )
    except Exception:
        raise HTTPException(401, "Please, Login")
    return {"message": "Authorize"}

def logout_handler(request: Request):
    try:
        req = request.cookies["authorization"]
        payload = get_decodeJWT(req)
        referee_id_connection.update_one({"username": payload.get("user_id")}, {"$set": {"expired": None}})
    except:
        raise HTTPException(400, "Something went wrong")
    return {"message": "Remove token successfully."}
    

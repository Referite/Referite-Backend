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
    payload = {
        "user_id": user_id,
        "expires": (datetime.now() + timedelta(days=1)).isoformat(),
    }
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
    """Only user can access"""
    try:
        req = request.headers["authorization"]
        if req == "dev":
            return {"message": "Welcome dev."}
        if audience_connection.find_one({"audience_token": req}):
            raise HTTPException(403, "Audience not allowed")
        payload = get_decodeJWT(req)
        user = referee_id_connection.find_one(
            {"username": payload.get("user_id")}, {"_id": 0}
        )
    except Exception:
        raise HTTPException(401, "Please, Login")
    if user is not None:
        return {"message": "Authorize"}


def allow_permission(request: Request):
    """Allow both audience and referee to access"""
    try:
        req = request.headers["authorization"]
        if req == "dev":
            return {"message": "Welcome dev."}
        if audience_connection.find_one({"audience_token": req}):
            return {"message": "Authorize Audience"}
        payload = get_decodeJWT(req)
        if referee_id_connection.find_one(
            {"username": payload.get("user_id")}, {"_id": 0}
        ):
            return {"message": "Authorize Referee"}
    except Exception:
        raise HTTPException(401, "Please, Login")


def logout_handler(request: Request):
    try:
        req = request.headers["authorization"]
        if req == "dev":
            return {"message": "Remove token successfully."}

        if audience_connection.find_one({"audience_token": req}):
            return {"message": "Remove token successfully."}

        payload = get_decodeJWT(req)
        if referee_id_connection.find_one(
            {"username": payload.get("user_id")}, {"_id": 0}
        ):
            referee_id_connection.update_one(
                {"username": payload.get("user_id")}, {"$set": {"expired": None}}
            )
            return {"message": "Remove token successfully."}
    except Exception as e:
        raise HTTPException(400, f"Something went wrong {e}")
    return {"message": "Remove token successfully."}

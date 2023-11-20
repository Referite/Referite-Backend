from datetime import datetime, timedelta
import sys
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from db import referee_id_connection

from auth.auth_handler import (
    check_password,
    check_user,
    create_access_token,
    check_token,
    logout_handler,
)
from models import TokenBody
from utils import error_handler

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

router = APIRouter(
    prefix="/api/auth", tags=["auth"], responses={404: {"description": "Not found"}}
)

expire_time = timedelta(days=1)
date = (datetime.now() + expire_time).isoformat()


@error_handler
@router.post("/token", status_code=201, response_model=TokenBody)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Receive username and password from body and check if user exists in database and password is correct
    then set cookie with the access token that expires in 1 day, after that redirect to homepage
    """
    if check_user(form_data) and check_password(form_data):
        access_token = create_access_token(form_data.username)
        referee_id_connection.update_one(
            {"username": form_data.username}, {"$set": {"expired": date}}
        )
        return {"access_token": access_token, "expired": date}
    raise HTTPException(401, "Please, Login")


@error_handler
@router.get("/logout", dependencies=[Depends(logout_handler)])
def logout():
    """Delete token"""
    return {"message": "Logout Successfully"}


@router.get("/test", dependencies=[Depends(check_token)])
def toast():
    """Test JWT token and cookie"""
    return {"message": "hello world"}

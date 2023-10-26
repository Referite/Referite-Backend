from fastapi import APIRouter, Depends, HTTPException, Response
from auth.auth_handler import check_password, check_user, create_access_token
from auth.cookie import OAuth2PasswordBearerWithCookie
import sys
from decouple import config
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))
from models import RefereeIdBody, SportScheduleBody
from utils import error_handler

router = APIRouter(prefix='/auth',
                   tags=["auth"],
                   responses={ 404: {"description": "Not found"}})

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/auth/token")

SECURE = config("SECURE", default=False, cast=bool)

@error_handler
@router.post('/token', status_code=201)
async def login(response: Response, id_body: RefereeIdBody):
    """
    Receive username and password from body and check if user exists in database and password is correct
    then set cookie with the access token that expires in 1 hour, after that redirect to homepage
    """
    if await check_user(id_body) and await check_password(id_body):
        access_token = create_access_token(id_body.username)
        response.set_cookie(key="access_token",
                            value=f"Bearer {access_token}", httponly=True, expires=3600, secure=SECURE)
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(401, "Invalid credentials")


@router.get('/test', dependencies=[Depends(oauth2_scheme)])
async def toast():
    """Test JWT token and cookie"""
    return {"message": "hello world"}
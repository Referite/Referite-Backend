from utils import error_handler
from models import RefereeIdBody, SportScheduleBody
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from auth.auth_handler import check_password, check_user, create_access_token, get_current_user
from auth.cookie import OAuth2PasswordBearerWithCookie
import sys
from decouple import config
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

router = APIRouter(prefix='/api/auth',
                   tags=["auth"],
                   responses={404: {"description": "Not found"}})

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="api/auth/token")

COOKIE_SECURE = config("SECURE", default=False, cast=bool)


@error_handler
@router.post('/token', status_code=201)
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Receive username and password from body and check if user exists in database and password is correct
    then set cookie with the access token that expires in 1 hour, after that redirect to homepage
    """
    if await check_user(form_data) and await check_password(form_data):
        access_token = create_access_token(form_data.username)
        response.set_cookie(key="access_token",
                            value=f"Bearer {access_token}", httponly=True, expires=3600, secure=COOKIE_SECURE)
        return {"message": "Login successful"}
    raise HTTPException(401, "Invalid credentials")


@error_handler
@router.get('/users')
async def get_user(user=Depends(get_current_user)):
    return user


@router.get('/test', dependencies=[Depends(oauth2_scheme)])
async def toast():
    """Test JWT token and cookie"""
    return {"message": "hello world"}

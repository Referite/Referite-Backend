from beanie import init_beanie
from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config
from db import Sport, SportSchedule, SportType, RefereeID
from auth.auth_handler import signJWT
from auth.cookie import OAuth2PasswordBearerWithCookie
from models import RefereeIdBody, SportScheduleBody
from utils import error_handler
from Enum.sportStatus import SportStatus
import bcrypt


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login/verify")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def connect_db():
    client = AsyncIOMotorClient(config("MONGO_URL", cast=str, default="mongodb://localhost:27017"),
                                tls=True,
                                tlsAllowInvalidCertificates=True)

    await init_beanie(database=client.referee, document_models=[SportType, SportSchedule, Sport, RefereeID])


@app.get('/1')
async def add_some_data():
    # main way to add data
    body1 = {
        "datetime": "2021-08-01T00:00:00",
        "sport": [{
            "sport_id": 1,
            "sport_name": "Football",
            "is_ceremonies": False,
            "sport_type": [
                {
                    "type_id": 1,
                    "type_name": "11v11",
                    "status": SportStatus.RECORDED
                },
                {
                    "type_id": 2,
                    "type_name": "7v7",
                    "status": SportStatus.TROPHY
                }
            ]}]
    }

    body2 = {
        "datetime": "2021-09-01T00:00:00",
        "sport": [{
            "sport_id": 1,
            "sport_name": "Football",
            "is_ceremonies": True,
            "sport_type": None
        }]}

    await SportSchedule(**body1).insert()
    await SportSchedule(**body2).insert()


@app.get('/2')
async def add_data():
    # alternative way to add data
    sport_type_body = {
        "type_id": 1,
        "type_name": "12v11",
        "status": SportStatus.CEREMONIES
    }

    sport_body = {
        "sport_id": 1,
        "sport_name": "Football",
        "is_ceremonies": False,
        "sport_type": [sport_type_body]
    }

    sport_schedule_body = {
        "datetime": "2021-08-01T00:00:00",
        "sport": [sport_body]
    }

    await Sport(**sport_body).insert()
    await SportType(**sport_type_body).insert()
    await SportSchedule(**sport_schedule_body).insert()

async def check_user(id_body: RefereeIdBody):
    """Check if user exists in database return boolean"""
    user = await RefereeID.find_one(RefereeID.username == str(id_body.username))
    return user is not None

async def check_password(id_body: RefereeIdBody):
    """Check if password is correct return boolean"""
    password = await RefereeID.find_one(RefereeID.username == str(id_body.username))
    return bool(bcrypt.checkpw(id_body.password.encode("utf-8"), password.password.encode("utf-8")))
    # return password is not None

def hash_password(id_body: RefereeIdBody):
    """Hash password"""
    return bcrypt.hashpw(id_body.password.encode("utf-8"), bcrypt.gensalt())

@app.get('/user/{username}/{password}')
async def get_user(username, password):
    """user for testing purpose"""
    #TODO Delete this once finish testing
    return await RefereeID.find_one(RefereeID.username == str(username), RefereeID.password == str(password))

@app.post('/create/user')
async def create_user(id_body: RefereeIdBody):
    """Create user for testing purpose"""
    data = {
        "username": id_body.username, 
        "password": hash_password(id_body).decode("utf-8")
    }
    user = RefereeID(**data)
    await user.insert()
    return {
        "status": "success",
        "message": "User created successfully",
        "data": user
    }

@error_handler
@app.post('/login/verify', status_code=201)
async def login(response: Response, id_body: RefereeIdBody):
    """
    Receive username and password from body and check if user exists in database and password is correct
    then set cookie with the access token, after that redirect to homepage
    """
    if await check_user(id_body) and await check_password(id_body):
        access_token = signJWT(id_body.username)
        response = RedirectResponse(
            url='/test/verify', status_code=302)  # change URL to homepage
        response.set_cookie(key="access_token",
                            value=f"Bearer {access_token}", httponly=True)
        return response
    raise HTTPException(401, "Invalid credentials")


@app.get('/test/verify', dependencies=[Depends(oauth2_scheme)])
async def toast():
    """Test JWT token and cookie"""
    return {"message": "hello world"}


@error_handler
@app.post('/sport_schedule/add')
async def add_sport_schedule(sport_schedule: SportScheduleBody):
    schedule = SportSchedule(**sport_schedule.model_dump())
    await schedule.insert()
    return {
        "status": "success",
        "message": "Sport schedule added successfully",
        "data": schedule
    }

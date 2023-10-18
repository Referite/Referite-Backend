from beanie import init_beanie
from fastapi import FastAPI, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config
from db import Sport, SportSchedule, SportType, RefereeID
from auth.auth_bearer import JWTBearer
from auth.auth_handler import signJWT
from models import RefereeIdBody
from Enum.sportStatus import SportStatus


app = FastAPI()


@app.on_event('startup')
async def connect_db():
    client = AsyncIOMotorClient(config("MONGO_URL", cast=str, default="mongodb://localhost:27017"),
                                tls=True,
                                tlsAllowInvalidCertificates=True)

    await init_beanie(database=client.referee, document_models=[SportType, SportSchedule, Sport, RefereeID])


@app.get('/1')
async def add_some_data():

    body = {
        "datetime": "2021-08-01T00:00:00",
        "sport": [{
            "sport_id": 1,
            "sport_name": "Football",
            "sport_type": [
                {
                    "type_id": 1,
                    "type_name": "11v11",
                    "status": SportStatus.CEREMONIES
                },
                {
                    "type_id": 2,
                    "type_name": "7v7",
                    "status": SportStatus.TROPHY
                }
            ]}]
    }

    await SportSchedule(**body).insert()


@app.get('/2')
async def add_data():
    sport_type_body = {
        "type_id": 1,
        "type_name": "12v11",
        "status": SportStatus.CEREMONIES
    }

    sport_body = {
        "sport_id": 1,
        "sport_name": "Football",
        "sport_type": [sport_type_body]
    }

    sport_schedjule_body = {
        "datetime": "2021-08-01T00:00:00",
        "sport": [sport_body]
    }

    await Sport(**sport_body).insert()
    await SportType(**sport_type_body).insert()
    await SportSchedule(**sport_schedjule_body).insert()


def check_user(id_body: RefereeIdBody):
    """Check if user exists in database return boolean"""
    return bool(
        RefereeID.find_one(
            {
                "username": str(id_body.username),
                "password": str(id_body.password),
            },
            {"_id": False},
        )
    )


@app.post('/login/verify', status_code=201)
async def login(id_body: RefereeIdBody):
    """Return a JWT token for the user_id
    if the user exists in the database
    Token format:{access_token: token}
    """
    try:
        if check_user(id_body):
            return signJWT(id_body.username)
    except Exception as e:
        raise HTTPException(500, "Something went wrong") from e

@app.get('/test/verify', dependencies=[Depends(JWTBearer())])
async def toast():
    return "hello world"
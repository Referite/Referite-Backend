from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config
from db import Sport, SportSchedule, SportType
from models import SportScheduleBody
from utils import error_handler

from Enum.sportStatus import SportStatus
app = FastAPI()


@app.on_event('startup')
async def connect_db():
    client = AsyncIOMotorClient(config("MONGO_URL", cast=str, default="mongodb://localhost:27017"),
                                tls=True,
                                tlsAllowInvalidCertificates=True)

    await init_beanie(database=client.referee, document_models=[SportType, SportSchedule, Sport])


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

    sport_schedjule_body = {
        "datetime": "2021-08-01T00:00:00",
        "sport": [sport_body]
    }

    await Sport(**sport_body).insert()
    await SportType(**sport_type_body).insert()
    await SportSchedule(**sport_schedjule_body).insert()

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

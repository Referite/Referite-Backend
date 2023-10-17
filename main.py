from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from db import Sport, SportSchedule, SportType
from typing import List, Dict, Union

from Enum.sportStatus import SportStatus
app = FastAPI()

@app.on_event('startup')
async def connect_db():
    client = AsyncIOMotorClient('mongodb+srv://referee:aBuxkgKjErZk9PZg@referite.4vc13sv.mongodb.net/?retryWrites=true&w=majority',
                                tls=True,
                                tlsAllowInvalidCertificates=True)

    await init_beanie(database=client.referee, document_models=[SportType, SportSchedule, Sport])


@app.get('/1')
async def add_some_data():

    body = {
        "datetime": "2021-08-01T00:00:00",
        "sport":[{
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
    pass
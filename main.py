from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from db import Sport, SportSchedule, SportType
from typing import List, Dict, Union

app = FastAPI()

@app.on_event('startup')
async def connect_db():
    client = AsyncIOMotorClient('mongodb+srv://referee:aBuxkgKjErZk9PZg@referite.4vc13sv.mongodb.net/?retryWrites=true&w=majority',
                                tls=True,
                                tlsAllowInvalidCertificates=True)

    await init_beanie(database=client.referee, document_models=[SportType, SportSchedule, Sport])


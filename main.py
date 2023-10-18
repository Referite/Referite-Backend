from beanie import init_beanie
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config
from db import Sport, SportSchedule, SportType, RefereeID
from models import RefereeIdBody
from Enum.sportStatus import SportStatus


app = FastAPI()


@app.on_event('startup')
async def connect_db():
    client = AsyncIOMotorClient(config("MONGO_URL", cast=str, default="mongodb://localhost:27017"),
                                tls=True,
                                tlsAllowIynvalidCertificates=True)

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

@app.post('/login/verify', status_code=201)
async def login(id_body: RefereeIdBody):
    try:
        name = str(id_body.username.decode())
        password = str(id_body.password.decode())

        if RefereeID.find_one({"username":name, "password":password}, {"_id": False}):
            return {"message": f"Welcome, {name} Login successfully"}
        else:
            return {"message": "Incorrect username or password, Please try again."}
    except Exception:
        raise HTTPException(500, "Something went wrong")
        



import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)
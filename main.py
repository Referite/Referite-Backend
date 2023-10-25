from beanie import init_beanie
from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config
from db import sport_schedule_connection
from auth.auth_handler import check_password, check_user, hash_password, create_access_token
from auth.cookie import OAuth2PasswordBearerWithCookie
from models import RefereeIdBody, SportScheduleBody
from utils import error_handler
from Enum.sportStatus import SportStatus
from router import auth, schedule
import bcrypt

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(schedule.router)
app.include_router(auth.router)


@app.get('/mock')
def add_some_data():
    """mock data using this endpoint"""
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

    sport_schedule_connection.insert_many([body1, body2])

    return {"message": "data mocked"}

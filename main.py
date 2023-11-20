from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import sport_schedule_connection
from Enum.sportStatus import SportStatus
from router import auth, record, schedule

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
app.include_router(record.router)
app.include_router(auth.router)


@app.get("/")
def index():
    return {"message": "Hello from Refrite✌️"}


@app.get("/api")
def api():
    return {"message": "Hello from Refrite✌️"}


@app.get("/mock")
def add_some_data():
    """mock data using this endpoint"""
    body1 = {
        "datetime": "2021-08-01T00:00:00",
        "sport": [
            {
                "sport_id": 1,
                "sport_name": "Football",
                "is_ceremonies": False,
                "sport_type": [
                    {
                        "type_id": 1,
                        "type_name": "11v11",
                        "status": SportStatus.RECORDED,
                    },
                    {"type_id": 2, "type_name": "7v7", "status": SportStatus.TROPHY},
                ],
            }
        ],
    }

    sport_schedule_connection.insert_many([body1, body2])

    return {"message": "data mocked"}

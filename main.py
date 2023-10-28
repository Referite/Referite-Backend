from fastapi import FastAPI
from router import schedule, record
from db import sport_schedule_connection
from Enum.sportStatus import SportStatus

app = FastAPI()

app.include_router(schedule.router)
app.include_router(record.router)



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

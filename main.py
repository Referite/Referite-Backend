from fastapi import FastAPI
from models import SportScheduleBody
from utils import error_handler
from utils import calculate_sport_status

from Enum.sportStatus import SportStatus
from db import sport_schedule_connection

app = FastAPI()


@app.get('/mock')
def add_some_data():
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

    sport_schedule_connection.insert_many([body1, body2])

    return {"message": "data mocked"}

@error_handler
@app.post('/sport_schedule/add', status_code=201)
def add_sport_schedule(sport_schedule: SportScheduleBody):
    sport_schedule_connection.insert_one(sport_schedule.model_dump())
    return {
        "status": "success",
        "message": "Sport schedule added successfully",
        "data": sport_schedule
    }

@error_handler
@app.get('/schedule/all')
def get_schedule():
    """
    get all schedule
    """
    # current_schedule = await SportSchedule.find_all().to_list()
    current_schedule = list(sport_schedule_connection.find({}, {"_id": 0}))

    print(current_schedule)

    for schedule in current_schedule:
        print(schedule, end="\n\n")
        for sport in schedule["sport"]:
            sport["sport_status"] = calculate_sport_status(sport["sport_type"])

    return {"schedule_list": current_schedule}

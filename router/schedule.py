from fastapi import APIRouter
from db import sport_schedule_connection


from models import SportScheduleBody
from utils import error_handler, calculate_sport_status

router = APIRouter(prefix='/api/schedule',
                   tags=["schedule"],
                   responses={ 404: {"description": "Not found"}})

@error_handler
@router.post('/add', status_code=201)
def add_sport_schedule(sport_schedule: SportScheduleBody):
    sport_schedule_connection.insert_one(sport_schedule.model_dump())
    return {
        "status": "success",
        "message": "Sport schedule added successfully",
        "data": sport_schedule
    }

@error_handler
@router.get('/all')
def get_schedule():
    """
    get all schedule
    """
    # current_schedule = await SportSchedule.find_all().to_list()
    current_schedule = list(sport_schedule_connection.find({}, {"_id": 0}))

    for schedule in current_schedule:
        for sport in schedule["sport"]:
            sport["sport_status"] = calculate_sport_status(sport["sport_type"])

    return {"schedule_list": current_schedule}

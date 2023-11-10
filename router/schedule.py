from fastapi import APIRouter, Depends
from auth.auth_handler import check_token

from db import sport_connection, sport_schedule_connection
from models import SportScheduleBody
from utils import calculate_sport_status, error_handler

router = APIRouter(
    prefix="/api/schedule",
    tags=["schedule"],
    responses={404: {"description": "Not found"}},
)


@error_handler
@router.post("/add", status_code=201, dependencies=[Depends(check_token)])
def add_sport_schedule(sport_schedule: SportScheduleBody):
    """endpoint to add sport schedule into db"""
    sport_schedule_connection.insert_one(sport_schedule.model_dump())
    return {
        "status": "success",
        "message": "Sport schedule added successfully",
        "data": sport_schedule,
    }


@error_handler
@router.get("/all", dependencies=[Depends(check_token)])
def get_schedule():
    """
    get all schedule
    """
    current_schedule = list(sport_schedule_connection.find({}, {"_id": 0}))

    for schedule in current_schedule:
        for sport in schedule["sport"]:
            sport["sport_status"] = calculate_sport_status(sport["sport_type"])

    return {"schedule_list": current_schedule}


@error_handler
@router.get("/sport", dependencies=[Depends(check_token)])
def get_all_sport():
    """
    get all sport
    """
    all_sport = list(sport_connection.find({}, {"sport_type": 0, "_id": 0}))

    return {"sport_list": all_sport}

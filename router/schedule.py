from fastapi import APIRouter
from db import sport_schedule_connection, sport_connection
import sys
from pathlib import Path
from models import SportScheduleBody
from utils import error_handler, calculate_sport_status


router = APIRouter(prefix='/api/schedule',
                   tags=["schedule"],
                   responses={ 404: {"description": "Not found"}})

@error_handler
@router.post('/add', status_code=201)
def add_sport_schedule(sport_schedule: SportScheduleBody):
    """endpoint to add sport schedule into db"""
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
    current_schedule = list(sport_schedule_connection.find({}, {"_id": 0}))

    for schedule in current_schedule:
        for sport in schedule["sport"]:
            sport["sport_status"] = calculate_sport_status(sport["sport_type"])

    return {"schedule_list": current_schedule}

@error_handler
@router.get('/sport')
def get_all_sport():
    """
    get all sport
    """
    all_sport = list(sport_connection.find({}, {"sport_type": 0, "_id": 0}))
    
    return {"sport_list": all_sport}
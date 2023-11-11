import datetime

from fastapi import APIRouter, Depends, HTTPException
from auth.auth_handler import check_token

from controllers.record_controller import (
    find_date_of_that_sport_type,
    get_ioc_data,
    record_medal_default_restriction,
    record_medal_repechage_restriction,
    update_medal_to_ioc,
    load_medal,
    find_status_of_that_sport_type
)
from db import sport_schedule_connection
from models import IocMedalBody, LoadMedalBody, RecordBody, VerifyBody, LoadMedalSportTypeBody, ParticipantBody
from utils import error_handler
from iso3166 import countries_by_name
from Enum.sportStatus import SportStatus

router = APIRouter(
    prefix="/api/record", tags=["record"], responses={404: {"description": "Not found"}}, dependencies=[Depends(check_token)]
)


@error_handler
@router.get("/detail/{date}/{sport_id}")
def get_detail(sport_id: int, date: datetime.datetime):
    """Retrieve sport detail by sport ID and match it with schedule data."""
    resp = get_ioc_data(sport_id)
    current_schedule = list(
        sport_schedule_connection.find(
            filter={"sport.sport_id": sport_id},
            projection={
                "_id": 0,
            },
        )
    )

    remove_idx = []

    formatted_competition_date = date.isoformat()

    for idx, types in enumerate(resp["sport_types"]):
        try:
            schedule_date = find_date_of_that_sport_type(
                current_schedule, types["type_id"], sport_id   
            )
            if schedule_date != formatted_competition_date:
                remove_idx.append(idx)
                continue

            types["competition_date"] =  schedule_date

            types["status"] = find_status_of_that_sport_type(
                current_schedule, types["type_id"], sport_id
            )
        except:
            remove_idx.append(idx)

    temp = []
    for idx, types in enumerate(resp["sport_types"]):
        if idx not in remove_idx:
            temp.append(types)

    resp["sport_types"] = temp

    for types in resp["sport_types"]:
        if types["status"] == f"{SportStatus.RECORDED}" and types["competition_date"] == formatted_competition_date:

            del types["participating_countries"]
            types["participants"] = load_medal(sport_id, types["type_id"])

    return resp


@error_handler
@router.post("/verify")
def verify_medal(verify_body: VerifyBody):
    """
    Record medal verification if it meets any restrictions and warn accordingly
    return a message dict: warning, message in this order or HTTP400 if invalid
    message = {"Message": "Successful",
                "Warning": "Appear if message have warning",
                "Monosport": "Appear if have message only 1 participant"}
    """
    verify = verify_body.model_dump()
    sport_name, participants = verify["sport_name"], verify["participants"]
    if not participants:
        raise HTTPException(400, "The participants can not be empty")
    repechage_list = ["wrestling", "boxing", "judo", "taekwondo"]
    gold, silver, bronze = 0, 0, 0
    for country in participants:
        gold += country["medal"]["gold"]
        silver += country["medal"]["silver"]
        bronze += country["medal"]["bronze"]
    if sport_name.lower() in repechage_list:
        message = record_medal_repechage_restriction(gold, silver, bronze)
    else:
        message = record_medal_default_restriction(gold, silver, bronze)
    if len(participants) == 1:
        message["Monosport"] = (
            f"There are only {len(participants)} country in this medal allocation, "
            f"Do you want to confirm this record?"
        )
    return message


@error_handler
@router.post("/medal/update")
def update(ioc_medal_body: IocMedalBody):
    """
    Update medal allocation in sota database
    """
    data = ioc_medal_body.model_dump()
    for medal_data in data["participants"]:
        medal_data["country"] = countries_by_name[medal_data["country"].upper()].alpha2
    return update_medal_to_ioc(data)


@error_handler
@router.get("/medal/load/{sport_id}", response_model=LoadMedalBody)
def load(sport_id: int):
    """
    Load medal allocation in sota database
    """

    return load_medal(sport_id)

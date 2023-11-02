from fastapi import APIRouter
from operator import itemgetter
from models import RecordBody, VerifyBody
from db import sport_schedule_connection
from controllers.record_controller import get_ioc_data, find_date_of_that_sport_type, record_medal_default_restriction, record_medal_repechage_restriction


router = APIRouter(
    prefix='/api/record',
    tags=["record"],
    responses={404: {"description": "Not found"}}
)


@router.get('/detail/{sport_id}')
def get_detail(sport_id: int):
    """Retrieve sport detail by sport ID and match it with schedule data."""
    resp = get_ioc_data(sport_id)
    current_schedule = list(sport_schedule_connection.find(filter={"sport.sport_id": sport_id, "sport.sport_type.type_id": 2}, projection={'_id': 0, 'sport.sport_type._id': 0, 'sport.revision_id': 0, 'sport.sport_type.revision_id': 0, 'sport._id': 0}))

    for types in resp['sport_types']:
         types["competition_date"] = find_date_of_that_sport_type(current_schedule, types['type_id'])

    return resp


@router.get('/verify')
def verify_medal(verify_body: VerifyBody):
    """
    Record medal verification if it meets any restrictions and warn accordingly
    return twos dict: warning, message in this order
    warning = {"Warning": "message"} or warning = {} depends on if it needs to warn or not
    message = {"Message": "message"}
    """
    verify = verify_body.model_dump()
    sport_name, participant = itemgetter('sport_name', 'participant')(verify)
    repechage_list = ["wrestling", "boxing", "judo", "taekwondo"]
    for country in participant:
        country_name = country['country']
        gold = country['medal']['gold']
        silver = country['medal']['silver']
        bronze = country['medal']['bronze']
        if sport_name.lower() in repechage_list:
            return record_medal_repechage_restriction(country_name, gold, silver, bronze)
        return record_medal_default_restriction(country_name, gold, silver, bronze)


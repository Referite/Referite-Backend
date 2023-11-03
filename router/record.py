from fastapi import APIRouter
from models import RecordBody, VerifyBody, IocMedalBody
from utils import error_handler
from db import sport_schedule_connection
from controllers.record_controller import get_ioc_data, find_date_of_that_sport_type, record_medal_default_restriction, record_medal_repechage_restriction


router = APIRouter(
    prefix='/api/record',
    tags=["record"],
    responses={404: {"description": "Not found"}}
)


@error_handler
@router.get('/detail/{sport_id}', response_model=RecordBody)
def get_detail(sport_id: int):
    """Retrieve sport detail by sport ID and match it with schedule data."""
    resp = get_ioc_data(sport_id)
    current_schedule = list(sport_schedule_connection.find(filter={"sport.sport_id": sport_id}, projection={'_id': 0, 'sport.sport_type._id': 0, 'sport.revision_id': 0, 'sport.sport_type.revision_id': 0, 'sport._id': 0}))

    for types in resp['sport_types']:
        types["competition_date"] = find_date_of_that_sport_type(
            current_schedule, types['type_id'])

    return resp


@error_handler
@router.post('/verify')
def verify_medal(verify_body: VerifyBody):
    """
    Record medal verification if it meets any restrictions and warn accordingly
    return twos dict: warning, message in this order
    warning = {"Warning": "message"} or warning = {} depends on if it needs to warn or not
    message = {"Message": "message"}
    """
    verify = verify_body.model_dump()
    sport_name, participant = verify['sport_name'], verify['participant']
    repechage_list = ["wrestling", "boxing", "judo", "taekwondo"]
    warning_countries = []
    message = {"Warning": "", "Message": "Medal allocation successful."}
    for country in participant:
        country_name = country['country']
        gold = country['medal']['gold']
        silver = country['medal']['silver']
        bronze = country['medal']['bronze']
        if sport_name.lower() in repechage_list:
            warning_country = record_medal_repechage_restriction(
                country_name, gold, silver, bronze)
            warning_countries.append(warning_country)
        else:
            warning_country = record_medal_default_restriction(
                country_name, gold, silver, bronze)
            if warning_country != '':
                warning_countries.append(warning_country)
    if warning_countries:
        message["Warning"] = f"Medal allocation for {warning_countries} deviates from default logic."
    return message

# @router.put('/medal/update/')
# def update_medal(medal: IocMedalBody):

# @router.put('/sport/update/')
# def update()

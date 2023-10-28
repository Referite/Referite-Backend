from fastapi import APIRouter
from models import RecordBody
from db import sport_schedule_connection
from controllers.record_controller import get_ioc_data, find_date_of_that_sport_type


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
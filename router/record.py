from fastapi import APIRouter, HTTPException
from models import SportScheduleBody
from db import sport_schedule_connection

router = APIRouter(
    prefix='/api/record',
    tags=["record"],
    responses={404: {"description": "Not found"}}
)

def get_sport_detail_by_id(sport_id: int):
    """Return sport data if sport ID exists"""
    # Example data:
    ioc_data = {
        "sport_id": 1,
        "sport_name": "Atheletics",
        "sport_summary": "The track programme includes sprints, middle-distance and long-distance events... Two kinds of event...",
        "sport_types": [
            {
                "type_id": 1,
                "type_name": "Men 100m",
                "participating_countries": [
                    "US", "DE", "JP"
                ]
            },
            {
                "type_id": 2,
                "type_name": "Women 100m",
                "participating_countries": [
                    "FR", "GR"
                ]
            }
        ],
        "participating_countries": [
            "US", "DE", "JP", "FR", "GR"
        ]
    }
    
    return ioc_data if sport_id == ioc_data["sport_id"] else None

@router.get('/detail/{sport_id}', response_model=dict)
def get_detail(sport_id: int):
    """Retrieve sport detail by sport ID and match it with schedule data."""
    sport_detail = get_sport_detail_by_id(sport_id)
    current_schedule = list(sport_schedule_connection.find({}, {"_id": 0}))
    
    # Initialize variables to store the datetime and sport details
    datetime = None
    sport_details = []

    for schedule in current_schedule:
        sport = schedule.get("sport", [{}])[0]  # Access the first sport entry (you can adjust if there are multiple)
        if sport.get("sport_id") == sport_id:
            datetime = schedule.get("datetime")
            break  # Stop searching once a match is found
    
    if datetime:
        for sport_type in sport_detail.get("sport_types", []):
            type_name = sport_type["type_name"]
            country = sport_type["participating_countries"]
            num_country = len(country)

            sport_details.append({
                "type_name": type_name,
                "participating_countries": country,
                "participating_countries_count": num_country,
                "datetime": datetime
            })
    
    return {"sport_types": sport_details}

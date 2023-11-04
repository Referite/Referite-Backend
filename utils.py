from typing import Dict, List

from Enum.sportStatus import SportStatus


def error_handler(f):
    def wrapper(*arg, **kwargs):
        try:
            return f(*arg, **kwargs)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    return wrapper


def calculate_sport_status(sport_types: List[Dict]):
    """
    calculate sport type with this following criteria
        COMPETITIVE -> any sport_type.status is competitive it will be competitive,
        TROPHY -> any sport_type.status is trophy it will be trophy,
        RECORDED -> all sport_type.status must be recorded then it will be
    """
    if sport_types is None:
        return SportStatus.CEREMONIES
    for sport_type in sport_types:
        if sport_type["status"] == SportStatus.COMPETITIVE:
            return SportStatus.COMPETITIVE
        if sport_type["status"] == SportStatus.TROPHY:
            return SportStatus.TROPHY
    return SportStatus.RECORDED

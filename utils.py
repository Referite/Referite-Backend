from typing import Dict, List

from Enum.sportStatus import SportStatus

import pycountry

mapping = {country.name: country.alpha_2 for country in pycountry.countries}
mapping["Kosovo"] = "XK"


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

    if not sport_types:
        return None

    for sport_type in sport_types:
        if sport_type["status"] == f"{SportStatus.CEREMONIES}":
            return SportStatus.CEREMONIES.value
        if sport_type["status"] == f"{SportStatus.COMPETITIVE}":
            return SportStatus.COMPETITIVE.value
        if sport_type["status"] == f"{SportStatus.TROPHY}":
            return SportStatus.TROPHY.value
    return SportStatus.RECORDED.value


def get_country_name(country_code: str):
    if country_code == "XK":
        return "Kosovo"
    return pycountry.countries.get(alpha_2=country_code).name


def get_country_code(country_code: str):
    return mapping.get(country_code)

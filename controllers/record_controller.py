import requests
from fastapi import HTTPException


def get_ioc_data(sport_id: int):
    """Return sport data if sport ID exists"""
    try:
        resp = requests.get(f'https://sota-backend.fly.dev/sport/{sport_id}')
        ioc_data = resp.json()
    except Exception as e:
        raise HTTPException(400, f"something went wrong with ioc_data: {e}")
    else:
        for sport_type in ioc_data['sport_types']:
            sport_type['participating_country_count'] = len(sport_type['participating_countries'])

    del ioc_data["sport_summary"]

    for sport_type in ioc_data['sport_types']:
        sport_type['participating_country_count'] = len(sport_type['participating_countries'])

    return ioc_data


def find_date_of_that_sport_type(schedule_data, type_id):
    """
        Find date of that sport type in schedule data
        """
    for schedule in schedule_data:
        for sport in schedule['sport']:
            for sport_type in sport['sport_type']:
                if sport_type['type_id'] == type_id:
                    return schedule['datetime']
    raise Exception("No sport that matches you request type_id")


def record_medal_default_restriction(gold_medal, silver_medal, bronze_medal):
    """Record medal from application with default restrictions"""
    warning = {}
    message = {"Message": "Medal allocation successful."}
    if gold_medal + silver_medal + bronze_medal > 3:
        # Issue a warning message, but continue with medal allocation
        warning["Warning"] = "Medal allocation deviates from default logic."

    if gold_medal >= 3 and silver_medal + bronze_medal > 0:
        raise HTTPException(400, "Invalid medal allocation.")
    elif gold_medal == 2 and silver_medal > 0:
        raise HTTPException(400, "Invalid medal allocation.")
    elif gold_medal == 1 and silver_medal >= 2 and bronze_medal > 0:
        raise HTTPException(400, "Invalid medal allocation.")
    return warning, message


def record_medal_repechage_restriction(gold_medal, silver_medal, bronze_medal):
    """
    Record medal from application with repêchage restrictions with bronze medal playoff
    (ref: https://en.wikipedia.org/wiki/List_of_ties_for_medals_at_the_Olympics#Ties_not_included_in_this_list)
    """
    warning = {}
    message = {"Message": "Medal allocation successful."}
    if gold_medal + silver_medal + bronze_medal > 4:
        # Issue a warning message, but continue with medal allocation
        warning["Warning"] = "Medal allocation deviates from default logic."

    if gold_medal >= 4 and silver_medal + bronze_medal > 0:
        raise HTTPException(400, "Invalid medal allocation.")
    elif gold_medal == 3 and silver_medal > 0:
        raise HTTPException(400, "Invalid medal allocation.")
    elif gold_medal == 2 and silver_medal >= 2 and bronze_medal > 0:
        raise HTTPException(400, "Invalid medal allocation.")
    elif gold_medal == 1 and silver_medal >= 3 and bronze_medal > 0:
        raise HTTPException(400, "Invalid medal allocation.")
    return warning, message




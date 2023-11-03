import requests
from fastapi import HTTPException
from typing import Dict
from Enum.sportStatus import SportStatus
from db import sport_schedule_connection


def get_ioc_data(sport_id: int):
    """Return sport data if sport ID exists"""
    try:
        resp = requests.get(f'https://sota-backend.fly.dev/sport/{sport_id}')
        ioc_data = resp.json()
    except Exception as e:
        raise HTTPException(400, f"something went wrong with ioc_data: {e}")
    else:
        for sport_type in ioc_data['sport_types']:
            sport_type['participating_country_count'] = len(
                sport_type['participating_countries'])

    del ioc_data["sport_summary"]

    for sport_type in ioc_data['sport_types']:
        sport_type['participating_country_count'] = len(
            sport_type['participating_countries'])

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


def record_medal_default_restriction(country_name, gold, silver, bronze):
    """Record medal from application with default restrictions"""
    warning_country = ''
    total_medals = gold + silver + bronze
    if total_medals != 3:
        warning_country = country_name
    invalid_combinations = [
        (gold >= 3 and silver + bronze > 0),
        (gold == 2 and silver > 0),
        (gold == 1 and silver >= 2 and bronze > 0),
    ]
    if any(invalid_combinations):
        raise HTTPException(400, "Invalid medal allocation.")
    return warning_country


def record_medal_repechage_restriction(country_name, gold, silver, bronze):
    """
    Record medal from application with repêchage restrictions with bronze medal playoff
    (ref: https://en.wikipedia.org/wiki/List_of_ties_for_medals_at_the_Olympics#Ties_not_included_in_this_list)
    """
    warning_country = ''
    total_medals = gold + silver + bronze
    if total_medals != 4:
        warning_country = country_name
    invalid_combinations = [
        (gold >= 4 and silver + bronze > 0),
        (gold == 3 and silver > 0),
        (gold == 2 and silver >= 2 and bronze > 0),
        (gold == 1 and silver >= 3 and bronze > 0),
    ]
    if any(invalid_combinations):
        raise HTTPException(
            400, f"Invalid medal allocation for {country_name}.")
    return warning_country


def update_status(sport_id: int, sport_type_id: int, status: SportStatus):
    """Update sport type status in sport schedule"""
    try:
        sport_schedule_connection.update_one({"_id": sport_id, }, {"$set": {"sport.$.sport_type.$.status": status}})
    except Exception as e:
        raise HTTPException(400, f"something went wrong with sport_type_id: {e}")
    else:
        return {"Message": "Status updated successfully."}
# def update_medal_to_ioc(medal: Dict):
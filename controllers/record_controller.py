from typing import Dict

import requests
from decouple import config
from fastapi import HTTPException

from db import sport_schedule_connection
from Enum.sportStatus import SportStatus


def get_ioc_data(sport_id: int):
    """Return sport data if sport ID exists"""
    try:
        resp = requests.get(f"https://sota-backend.fly.dev/sport/{sport_id}")
        ioc_data = resp.json()
    except Exception as e:
        raise HTTPException(400, f"something went wrong with ioc_data: {e}")
    else:
        for sport_type in ioc_data["sport_types"]:
            sport_type["participating_country_count"] = len(
                sport_type["participating_countries"]
            )

    del ioc_data["sport_summary"]

    for sport_type in ioc_data["sport_types"]:
        sport_type["participating_country_count"] = len(
            sport_type["participating_countries"]
        )

    return ioc_data


def find_date_of_that_sport_type(schedule_data, type_id):
    """
    Find date of that sport type in schedule data
    """
    for schedule in schedule_data:
        for sport in schedule["sport"]:
            for sport_type in sport["sport_type"]:
                if sport_type["type_id"] == type_id:
                    return schedule["datetime"]
    raise Exception("No sport that matches you request type_id")


def record_medal_default_restriction(gold, silver, bronze):
    """Record medal from application with default restrictions"""
    message = {"Message": "Medal allocation successful."}
    total_medals = gold + silver + bronze
    # Invalid
    if gold >= 3 and silver + bronze > 0:
        raise HTTPException(400, f"There are {gold} gold medals awarded, No silver or bronze medal will be given.")
    elif gold == 2 and silver > 0:
        raise HTTPException(400, f"There are {gold} gold medals awarded, No silver medal will be given.")
    elif gold == 1 and silver >= 2 and bronze > 0:
        raise HTTPException(400, f"There are {silver} silver medals awarded, No bronze medal will be given.")
    # Warnings
    if total_medals > 3 or total_medals == 0:
        message["Warning"] = f"There are {total_medals} medals awarded, Do you want to confirm this record?"
    elif gold >= 2:
        message["Warning"] = f"There are {gold} gold medals awarded, Do you want to confirm this record?"
    elif silver >= 2:
        message["Warning"] = f"There are {silver} silver medals awarded, Do you want to confirm this record?"
    elif bronze >= 2:
        message["Warning"] = f"There are {bronze} bronze medals awarded, Do you want to confirm this record?"
    return message


def record_medal_repechage_restriction(gold, silver, bronze):
    """
    Record medal from application with repêchage restrictions with bronze medal playoff
    (ref: https://en.wikipedia.org/wiki/List_of_ties_for_medals_at_the_Olympics#Ties_not_included_in_this_list)
    """
    message = {"Message": "Medal allocation successful."}
    total_medals = gold + silver + bronze
    # Invalid
    if gold >= 4 and silver + bronze > 0:
        raise HTTPException(400, f"There are {gold} gold medals awarded, No silver or bronze medal will be given.")
    elif gold == 3 and silver > 0:
        raise HTTPException(400, f"There are {gold} gold medals awarded, No silver medal will be given.")
    elif (gold == 2 and silver >= 2 and bronze) > 0 or (gold == 1 and silver >= 3 and bronze > 0):
        raise HTTPException(400, f"There are {silver} silver medals awarded, No bronze medal will be given.")
    # Warnings
    if total_medals > 4 or total_medals == 0:
        message["Warning"] = f"There are {total_medals} medals awarded, Do you want to confirm this record?"
    elif gold >= 2:
        message["Warning"] = f"There are {gold} gold medals awarded, Do you want to confirm this record?"
    elif silver >= 2:
        message["Warning"] = f"There are {silver} silver medals awarded, Do you want to confirm this record?"
    elif bronze >= 3:
        message["Warning"] = f"There are {bronze} bronze medals awarded, Do you want to confirm this record?"
    return message


def update_status(sport_id: int, sport_type_id: int, status: SportStatus):
    """Update sport type status in sport schedule"""
    try:
        sport_schedule_connection.update_one(
            {"sport.sport_id": sport_id, "sport.sport_type.type_id": sport_type_id},
            {"$set": {"sport.$[i].sport_type.$[j].status": status}},
            array_filters=[{"i.sport_id": sport_id}, {"j.type_id": sport_id}],
        )
    except Exception as e:
        raise HTTPException(400, f"something went wrong: {e}")
    else:
        return {"Message": "Status updated successfully."}


def update_medal_to_ioc(medal: Dict):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {config("IOC_ACCESS_TOKEN", cast=str, default="")}',
    }

    resp = requests.post(
        "https://sota-backend.fly.dev/medals/update_medal", headers=headers, json=medal
    )

    if resp.status_code != 200:
        return resp.json()
    data = resp.json()["Success"]

    update_status(data["sport_id"], data["sport_type_id"], str(SportStatus.RECORDED))

    return resp.json()

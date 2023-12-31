from typing import Dict

import requests
from decouple import config
from fastapi import HTTPException

from db import sport_schedule_connection
from Enum.sportStatus import SportStatus

from utils import get_country_name


def get_ioc_data(sport_id: int):
    """Return sport data if sport ID exists"""
    try:
        resp = requests.get(f"https://sota-backend.fly.dev/sport/{sport_id}")
        ioc_data = resp.json()
    except Exception as e:
        raise HTTPException(400, f"something went wrong with ioc_data: {e}") from e

    del ioc_data["sport_summary"]

    for sport_type in ioc_data["sport_types"]:
        sport_type["participating_country_count"] = len(
            sport_type["participating_countries"]
        )
        sport_type["participating_countries"] = list(
            map(
                lambda country: get_country_name(country),
                sport_type["participating_countries"],
            )
        )

    return ioc_data


def find_date_of_that_sport_type(schedule_data, type_id, sport_id):
    """
    Find date of that sport type in schedule data
    """
    for schedule in schedule_data:
        for sport in schedule["sport"]:
            if sport["sport_id"] != sport_id:
                continue

            for sport_type in sport["sport_type"]:
                if sport_type["type_id"] == type_id:
                    return schedule["datetime"]
    raise HTTPException(
        400, f"No sport that matches you request type_id of sport {sport_id}"
    )


def find_status_of_that_sport_type(schedule_data, type_id, sport_id):
    """
    Find status of that sport type in schedule data
    """
    for schedule in schedule_data:
        for sport in schedule["sport"]:
            if sport["sport_id"] != sport_id:
                continue
            for sport_type in sport["sport_type"]:
                if sport_type["type_id"] == type_id:
                    return sport_type["status"]
    raise HTTPException(
        400, f"No sport that matches you request type_id of sport {sport_id}"
    )


def record_medal_default_restriction(gold, silver, bronze):
    """Record medal from application with default restrictions"""
    message = {"Message": "Medal allocation successful."}
    total_medals = gold + silver + bronze
    # Invalid
    if total_medals == 0:
        raise HTTPException(
            400,
            f"""There are {total_medals} medals awarded, no need to record this body.""",
        )
    elif gold >= 10 or silver >= 10 or bronze >= 10:
        raise HTTPException(
            400,
            f"There are 10 or more medals of a specific type awarded to a single country, "
            f"This should not be possible.",
        )
    elif gold >= 3 and silver + bronze > 0:
        raise HTTPException(
            400,
            f"""There are {
                            gold} gold medals awarded, No silver or bronze medal will be given.""",
        )
    elif gold == 2 and silver > 0:
        raise HTTPException(
            400,
            f"""There are {gold} gold medals awarded, No silver medal will be given.""",
        )
    elif gold == 1 and silver >= 2 and bronze > 0:
        raise HTTPException(
            400,
            f"""There are {
                            silver} silver medals awarded, No bronze medal will be given.""",
        )
    # Warnings
    if total_medals > 3:
        message[
            "Warning"
        ] = f"There are {total_medals} medals awarded, Do you want to confirm this record?"
    elif gold >= 2:
        message[
            "Warning"
        ] = f"There are {gold} gold medals awarded, Do you want to confirm this record?"
    elif silver >= 2:
        message[
            "Warning"
        ] = f"There are {silver} silver medals awarded, Do you want to confirm this record?"
    elif bronze >= 2:
        message[
            "Warning"
        ] = f"There are {bronze} bronze medals awarded, Do you want to confirm this record?"
    return message


def record_medal_repechage_restriction(gold, silver, bronze):
    """
    Record medal from application with repêchage restrictions with bronze medal playoff
    (ref: https://en.wikipedia.org/wiki/List_of_ties_for_medals_at_the_Olympics#Ties_not_included_in_this_list)
    """
    message = {"Message": "Medal allocation successful."}
    total_medals = gold + silver + bronze
    # Invalid
    if total_medals == 0:
        raise HTTPException(
            400,
            f"""There are {total_medals} medals awarded, no need to record this body.""",
        )
    elif gold >= 10 or silver >= 10 or bronze >= 10:
        raise HTTPException(
            400,
            f"""There are 10 or more medals of a specific type awarded to a single country, This should not be possible.""",
        )
    elif gold >= 4 and silver + bronze > 0:
        raise HTTPException(
            400,
            f"""There are {
                gold} gold medals awarded, No silver or bronze medal will be given.""",
        )
    elif gold == 3 and silver > 0:
        raise HTTPException(
            400,
            f"""There are {
                gold} gold medals awarded, No silver medal will be given.""",
        )
    elif (gold == 2 and silver >= 2 and bronze) > 0 or (
        gold == 1 and silver >= 3 and bronze > 0
    ):
        raise HTTPException(
            400,
            f"""There are {
                silver} silver medals awarded, No bronze medal will be given.""",
        )
    # Warnings
    if total_medals > 4:
        message[
            "Warning"
        ] = f"There are {total_medals} medals awarded, Do you want to confirm this record?"
    elif gold >= 2:
        message[
            "Warning"
        ] = f"There are {gold} gold medals awarded, Do you want to confirm this record?"
    elif silver >= 2:
        message[
            "Warning"
        ] = f"There are {silver} silver medals awarded, Do you want to confirm this record?"
    elif bronze >= 3:
        message[
            "Warning"
        ] = f"There are {bronze} bronze medals awarded, Do you want to confirm this record?"
    return message


def update_status(sport_id: int, sport_type_id: int, status: SportStatus):
    """Update sport type status in sport schedule"""
    try:
        query = {
            "sport.sport_id": sport_id,
            "sport.sport_type.type_id": sport_type_id,
            "sport.sport_type.status": "TROPHY",
        }
        all_schedule = sport_schedule_connection.find(query)
        replace_date = find_date_of_that_sport_type(
            all_schedule, sport_type_id, sport_id
        )
        query["datetime"] = replace_date
        to_replace = sport_schedule_connection.find_one(query)

        for sport in to_replace["sport"]:
            if sport["sport_id"] == sport_id:
                print(sport)
                for types in sport["sport_type"]:
                    if types["type_id"] == sport_type_id and types["status"] == str(
                        SportStatus.TROPHY
                    ):
                        types["status"] = status
                        break

        res = sport_schedule_connection.replace_one(query, to_replace)

    except Exception as e:
        raise HTTPException(400, f"something went wrong: {e}")
    else:
        return {"Message": "Status updated successfully.", "Response": res}


def update_medal_to_ioc(medal: Dict):
    """Update medal to IOC with Authorization token"""
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


def load_medal(sport_id: int, type_id):
    """Load medal from IOC for showing in load detail page."""
    resp = requests.get(
        f"https://sota-backend.fly.dev/medal/s/{sport_id}/t/{type_id}"
    ).json()
    if resp == {}:
        raise HTTPException(400, "Please, record medal before load detail")

    for each_type in resp["individual_countries"]:
        each_type["country"] = each_type["country_name"]
        each_type["medal"] = {
            "gold": each_type["gold"],
            "silver": each_type["silver"],
            "bronze": each_type["bronze"],
        }
        del each_type["gold"]
        del each_type["silver"]
        del each_type["bronze"]
        del each_type["country_name"]
        del each_type["country_code"]

    return resp["individual_countries"]

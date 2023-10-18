from beanie import Document
from Enum.sportStatus import SportStatus
from enum import Enum
from typing import List
import datetime

class SportType(Document):
    type_id: int
    type_name: str
    status: SportStatus

    class Config:
        arbitrary_types_allowed = True

class Sport(Document):
    sport_id: int
    sport_name: str
    sport_type: List[SportType]

class SportSchedule(Document):
    datetime: datetime.datetime
    sport: List[Sport]

class RefereeID(Document):
    username: str
    password: str
    
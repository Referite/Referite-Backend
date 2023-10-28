from pydantic import BaseModel, validator
from Enum.sportStatus import SportStatus
from typing import List, Optional
import datetime

class SportTypeBody(BaseModel):
    type_id: int
    type_name: str
    status: SportStatus


class SportBody(BaseModel):
    sport_id: int
    sport_name: str
    sport_type: Optional[List[SportTypeBody]]
    is_ceremonies: bool

    @validator('sport_type', always=True)
    def validate(cls, value, values):
        if values.get("is_ceremonies") and value:
            raise ValueError("sport_type should not be present when is_ceremonies is True")
        return value

class SportScheduleBody(BaseModel):
    datetime: datetime.datetime
    sport: List[SportBody]

class SportTypeRecordBody(BaseModel):
    type_id: int
    type_name: str
    competition_date: datetime.date
    participating_country_count: int
    participating_country: List[str]

class RecordBody(BaseModel):
    sport_id: int
    sport_name: str
    sport_types: List[SportTypeRecordBody]

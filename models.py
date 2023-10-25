from pydantic import BaseModel, validator, field_validator
from Enum.sportStatus import SportStatus
from typing import List, Optional
import datetime

class Schedule(BaseModel):
    pass

class RefereeIdBody(BaseModel):
    username: str
    password: str
class SportTypeBody(BaseModel):
    type_id: int
    type_name: str
    status: str

    @field_validator('status')
    @classmethod
    def status_must_be_enum(cls, v: str):
        try:
            SportStatus(v)
        except AssertionError as e:
            raise ValueError("status must be ['CEREMONIES', 'COMPETITIVE', 'TROPHY', 'RECORDED']")
        return v

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


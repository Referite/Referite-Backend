import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, field_validator, validator

from Enum.sportStatus import SportStatus


class RefereeIdBody(BaseModel):
    username: str
    password: str


class SportTypeBody(BaseModel):
    type_id: int
    type_name: str
    status: str

    @field_validator("status")
    @classmethod
    def status_must_be_enum(cls, v: str):
        try:
            SportStatus(v)
        except AssertionError as e:
            raise ValueError(
                "status must be ['CEREMONIES', 'COMPETITIVE', 'TROPHY', 'RECORDED']"
            )
        return v


class SportBody(BaseModel):
    sport_id: int
    sport_name: str
    sport_type: Optional[List[SportTypeBody]]
    is_ceremonies: bool

    @validator("sport_type", always=True)
    def validate(cls, value, values):
        if values.get("is_ceremonies") and value:
            raise ValueError(
                "sport_type should not be present when is_ceremonies is True"
            )
        return value


class SportScheduleBody(BaseModel):
    datetime: datetime.datetime
    sport: List[SportBody]


class SportTypeRecordBody(BaseModel):
    type_id: int
    type_name: str
    competition_date: datetime.datetime
    participating_country_count: int
    participating_countries: List[str]


class RecordBody(BaseModel):
    sport_id: int
    sport_name: str
    sport_types: List[SportTypeRecordBody]


class MedalBody(BaseModel):
    gold: int
    silver: int
    bronze: int


class ParticipantBody(BaseModel):
    country: str
    medal: MedalBody


class VerifyBody(BaseModel):
    sport_name: str
    participants: List[ParticipantBody]


class IocMedalBody(BaseModel):
    sport_id: int
    sport_type_id: int
    participants: List[ParticipantBody]


class LoadMedalSportTypeBody(BaseModel):
    type_id: int
    type_name: str
    participating_country_count: int
    competition_date: datetime.datetime
    participants: List[ParticipantBody]


class LoadMedalBody(BaseModel):
    sport_id: int
    sport_name: str
    sport_types: List[LoadMedalSportTypeBody]

class TokenBody(BaseModel):
    access_token: str
    expired: str


from beanie import Document
from Enum.sportStatus import SportStatus
from typing import List, Optional
from pydantic import validator
from pymongo import MongoClient
from decouple import config
import datetime

# class SportType(Document):
#     type_id: int
#     type_name: str
#     status: SportStatus

#     class Config:
#         arbitrary_types_allowed = True

# class Sport(Document):
#     sport_id: int
#     sport_name: str
#     sport_type: Optional[List[SportType]]
#     is_ceremonies: bool

#     @validator('sport_type', always=True)
#     def validate(cls, value, values):
#         if values.get("is_ceremonies") and value:
#             raise ValueError("sport_type should not be present when is_ceremonies is True")
#         return value
    

# class SportSchedule(Document):
#     datetime: datetime.datetime
#     sport: List[Sport]


client = MongoClient(config("MONGO_URL", cast=str, default="mongodb://localhost:27017"), tls=True, tlsAllowInvalidCertificates=True)

mongo_connection = client['referee']

sport_schedule_connection = mongo_connection['SportSchedule']
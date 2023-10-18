from pydantic import BaseModel

class Schedule(BaseModel):
    pass

class RefereeIdBody(BaseModel):
    name: str
    password: str
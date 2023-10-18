from pydantic import BaseModel

class Schedule(BaseModel):
    pass

class RefereeIdBody(BaseModel):
    username: str
    password: str
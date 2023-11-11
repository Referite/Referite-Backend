from decouple import config
from pymongo import MongoClient

client = MongoClient(
    config("MONGO_URL", cast=str, default="mongodb://localhost:27017"),
    tls=True,
    tlsAllowInvalidCertificates=True,
)

mongo_connection = client["referee"]

sport_schedule_connection = mongo_connection["SportSchedule"]
sport_connection = mongo_connection["Sport"]
referee_id_connection = mongo_connection["RefereeID"]
audience_connection = mongo_connection["AudienceToken"]

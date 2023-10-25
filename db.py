from pymongo import MongoClient
from decouple import config

client = MongoClient(config("MONGO_URL", cast=str, default="mongodb://localhost:27017"), tls=True, tlsAllowInvalidCertificates=True)

mongo_connection = client['referee']

sport_schedule_connection = mongo_connection['SportSchedule']
sport_connection = mongo_connection['Sport']
sport_type_connection = mongo_connection['SportType']
referee_id_connection = mongo_connection['RefereeID']

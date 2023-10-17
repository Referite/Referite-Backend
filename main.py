from pymongo import MongoClient
# from dotenv import load_dotenv
# import os

# get username and password from .env file
# load_dotenv(".env")
# username = os.getenv("username")
# password = os.getenv("password")

client = MongoClient(
    f"mongodb+srv://referee:aBuxkgKjErZk9PZg@referite.4vc13sv.mongodb.net/?retryWrites=true&w=majority",
    tls=True,
    tlsAllowInvalidCertificates=True)


# use database name 
db = client["referee"]
# use collection name 
collection = db["referee"]

test = collection.find_one({"eiei": "iiiiiiiiii"})
test["_id"] = str(test["_id"])
print(test)
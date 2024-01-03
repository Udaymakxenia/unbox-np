from pymongo import MongoClient
from app.config import(
    MONGODB_URL
)

def mongoClient():
    mongoClient = MongoClient(MONGODB_URL)
    return mongoClient["unbox_np_db"]


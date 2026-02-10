from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URI)
db = client["finance_tracker_db"]

print("Connected to db:", db.name)
print("COLLECTIONS:", db.list_collection_names())

transactions_col = db["transactions"]
from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URI)
db = client["finance_tracker_db"]

transactions_col = db["transactions"]
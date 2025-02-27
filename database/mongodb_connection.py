import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongodb_url = os.getenv("MONGODB_URL")
mongodb_name = os.getenv("MONGODB_NAME")

client = MongoClient(mongodb_url)
database = client[mongodb_name]

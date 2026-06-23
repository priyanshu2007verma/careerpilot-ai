from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(
    os.getenv("MONGO_URI")
)

db = client["careerpilot_ai"]

users = db["users"]
resumes = db["resumes"]
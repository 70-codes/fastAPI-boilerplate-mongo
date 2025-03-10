from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "fastapi-mongo-biolerplate"

# Async client for FastAPI
client = AsyncIOMotorClient(MONGO_URI)
database = client[DATABASE_NAME]

# # Sync client (if needed) though this is an IO blocking operation hence may make the server to be slower
# sync_client = MongoClient(MONGO_URI)
# sync_db = sync_client[DATABASE_NAME]


async def get_database():
    """Returns the database instance for dependency injection."""
    return database

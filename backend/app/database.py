from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    client = None
    db = None
    
    @classmethod
    async def connect(cls):
        if cls.client is None:
            mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
            cls.client = AsyncIOMotorClient(mongodb_url)
            cls.db = cls.client[os.getenv("DATABASE_NAME", "meitei_dictionary")]
        return cls.db
    
    @classmethod
    async def close(cls):
        if cls.client:
            cls.client.close()
            cls.client = None
            cls.db = None

async def get_db():
    return await Database.connect()
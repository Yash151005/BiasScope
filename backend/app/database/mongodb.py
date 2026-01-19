"""
MongoDB database connection and utilities
"""

from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

# Global database client
client: Optional[AsyncIOMotorClient] = None
database = None


async def get_database():
    """Get MongoDB database instance"""
    global client, database

    if database is None:
        try:
            client = AsyncIOMotorClient(settings.mongodb_url)
            database = client[settings.mongodb_database]
            logger.info(f"Connected to MongoDB database: {settings.mongodb_database}")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise

    return database


async def close_database():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        logger.info("MongoDB connection closed")

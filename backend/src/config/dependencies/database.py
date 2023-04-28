import motor.motor_asyncio

from src.config.settings import Settings

settings = Settings()


def get_database():
    """Retrieves database connection object"""
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.db_uri)
    yield client[settings.db_name]

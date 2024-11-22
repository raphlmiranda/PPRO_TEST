import motor.motor_asyncio
from beanie import init_beanie

from src.infra.configs.local import Settings
from src.domain.entities.file_data import FileData
from src.domain.entities.email_file import EmailFile


settings = Settings()

async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        settings.MONGO_URI
    )

    await init_beanie(
        database=client.db_name,
        document_models=[EmailFile]
    )
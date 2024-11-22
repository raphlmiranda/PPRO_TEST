from fastapi import FastAPI

from src.infra.database.mongo import init_db
from src.router.file_router import file_router

async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(file_router)

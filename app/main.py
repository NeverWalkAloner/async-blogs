import uvicorn
from contextlib import asynccontextmanager
from app.models.database import database
from app.routers import posts, users
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(posts.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

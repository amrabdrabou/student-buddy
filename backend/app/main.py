from sqlalchemy import text
from fastapi import FastAPI, Depends
from app.core.config import Settings, get_settings
from contextlib import asynccontextmanager
from app.core.db_setup import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text("SELECT 1"))

    print("Database connected")
    
    yield
    
    await engine.dispose()
    print("Database connection closed")


app = FastAPI(
    lifespan=lifespan,
    title="Student Buddy API",
    description="AI-Powered Study Assistant",
    version="1.0.0",
)

@app.get("/info")
def info(settings: Settings = Depends(get_settings)):
    return {
        "environment": settings.environment,
        "debug": settings.debug,
    }
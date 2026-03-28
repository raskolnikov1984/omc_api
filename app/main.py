from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.endpoints.leads import leads
from app.database import get_db

app = FastAPI()


app.include_router(leads.router, prefix="/api/v1", tags=["create_lead"])


@app.get("/api/v1/")
async def root():
    return {"message": "Welcome To OMC LEAD's"}


@app.get("/api/v1/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        database_status = "healthy"
    except Exception:
        database_status = "unhealthy"

    return {
        "status": "healthy" if database_status == "healthy" else "unhealthy",
        "database": database_status,
    }

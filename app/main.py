from fastapi import FastAPI
from .api.v1.endpoints.leads import leads

app = FastAPI()


app.include_router(leads.router, prefix="/api/v1", tags=["create_lead"])


@app.get("/api/v1/")
async def root():
    return {
        "message": "Welcome To OMC LEAD's"
    }

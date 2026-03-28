from fastapi import APIRouter, status
from app.schemes.leads import LeadScheme


router = APIRouter()

leads = []


@router.post("/leads", status_code=status.HTTP_201_CREATED)
async def create_lead(lead: LeadScheme):
    """
    Create a new lead
    """
    leads.append(lead)

    return {
        "message": "successful"
    }

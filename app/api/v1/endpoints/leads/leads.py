from datetime import date, datetime

from fastapi import APIRouter, HTTPException, Query, status
from app.schemes.leads import LeadScheme


router = APIRouter()

leads = []


@router.post("/leads", status_code=status.HTTP_201_CREATED)
async def create_lead(lead: LeadScheme):
    """
    Create a new lead
    """
    lead_dict = lead.model_dump()
    lead_dict["created_at"] = datetime.now()
    lead_id = len(leads) + 1
    lead_dict["id"] = lead_id
    leads.append(lead_dict)

    return {"id": lead_id, "message": "successful"}


@router.get("/leads/{lead_id}")
async def get_lead(lead_id: int):
    """
    Get a lead by ID
    """
    if lead_id < 1 or lead_id > len(leads):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found"
        )

    return leads[lead_id - 1]


@router.get("/leads")
async def get_leads(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    source: str | None = Query(None),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    order_dir: str = Query("desc", pattern="^(asc|desc)$"),
):
    """
    Get all leads with pagination, filtering and ordering
    """
    filtered_leads = leads.copy()

    if source:
        filtered_leads = [
            l for l in filtered_leads if l.get("source") == source
        ]

    if start_date:
        filtered_leads = [
            l
            for l in filtered_leads
            if l.get("created_at") and l["created_at"].date() >= start_date
        ]

    if end_date:
        filtered_leads = [
            l
            for l in filtered_leads
            if l.get("created_at") and l["created_at"].date() <= end_date
        ]

    reverse_order = order_dir == "desc"
    filtered_leads.sort(
        key=lambda x: x.get(
            "created_at") or datetime.min, reverse=reverse_order
    )

    total = len(filtered_leads)
    total_pages = (total + limit - 1) // limit
    start = (page - 1) * limit
    end = start + limit
    items = filtered_leads[start:end]

    return {
        "items": items,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
    }

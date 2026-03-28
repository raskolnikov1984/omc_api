from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemes.leads import LeadScheme, LeadUpdateScheme
from app.services.leads_service import LeadService

router = APIRouter()


@router.post("/leads", status_code=status.HTTP_201_CREATED)
async def create_lead(
    lead: LeadScheme,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new lead
    """
    service = LeadService(db)
    created_lead = await service.create_lead(lead)

    return {"id": created_lead.id, "created_at": created_lead.created_at}


@router.get("/leads/{lead_id}")
async def get_lead(
    lead_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Get a lead by ID
    """
    service = LeadService(db)
    lead = await service.get_lead_by_id(lead_id)

    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found"
        )

    return {
        "id": lead.id,
        "name": lead.name,
        "email": lead.email,
        "phone": lead.phone,
        "source": lead.source,
        "target_product": lead.target_product,
        "budget": lead.budget,
        "created_at": lead.created_at,
    }


@router.patch("/leads/{lead_id}")
async def update_lead(
    lead_id: int,
    lead: LeadUpdateScheme,
    db: AsyncSession = Depends(get_db),
):
    """
    Update an existing lead
    """
    service = LeadService(db)
    updated_lead = await service.update_lead(lead_id, lead)

    if not updated_lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found"
        )

    return {
        "id": updated_lead.id,
        "name": updated_lead.name,
        "email": updated_lead.email,
        "phone": updated_lead.phone,
        "source": updated_lead.source,
        "target_product": updated_lead.target_product,
        "budget": updated_lead.budget,
        "created_at": updated_lead.created_at,
    }


@router.get("/leads")
async def get_leads(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    source: str | None = Query(None),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    order_dir: str = Query("desc", pattern="^(asc|desc)$"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get all leads with pagination, filtering and ordering
    """
    service = LeadService(db)

    start_datetime = (
        datetime.combine(start_date, datetime.min.time()) if start_date else None
    )
    end_datetime = datetime.combine(end_date, datetime.max.time()) if end_date else None

    leads = await service.get_leads(
        source=source,
        start_date=start_datetime,
        end_date=end_datetime,
        order_desc=order_dir == "desc",
    )

    total = len(leads)
    total_pages = (total + limit - 1) // limit
    start = (page - 1) * limit
    end = start + limit
    items = leads[start:end]

    return {
        "items": [
            {
                "id": lead.id,
                "name": lead.name,
                "email": lead.email,
                "phone": lead.phone,
                "source": lead.source,
                "target_product": lead.target_product,
                "budget": lead.budget,
                "created_at": lead.created_at,
            }
            for lead in items
        ],
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
    }


@router.delete("/leads/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lead(
    lead_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a lead by ID
    """
    service = LeadService(db)
    deleted = await service.delete_lead(lead_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found"
        )

from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import LeadSQL
from app.schemes.leads import LeadScheme


class LeadService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_lead(self, data: LeadScheme) -> LeadSQL:
        lead = LeadSQL(
            name=data.name,
            email=data.email,
            phone=data.phone,
            source=data.source,
            target_product=data.target_product,
            budget=data.budget,
            created_at=datetime.now(),
        )
        self.session.add(lead)
        await self.session.commit()
        await self.session.refresh(lead)
        return lead

    async def get_lead_by_id(self, lead_id: int) -> Optional[LeadSQL]:
        result = await self.session.execute(
            select(LeadSQL).where(LeadSQL.id == lead_id)
        )
        return result.scalar_one_or_none()

    async def get_leads(
        self,
        source: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        order_desc: bool = True,
    ) -> list[LeadSQL]:
        query = select(LeadSQL)

        if source:
            query = query.where(LeadSQL.source == source)

        if start_date:
            query = query.where(LeadSQL.created_at >= start_date)

        if end_date:
            query = query.where(LeadSQL.created_at <= end_date)

        query = query.order_by(
            LeadSQL.created_at.desc() if order_desc else LeadSQL.created_at.asc()
        )

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def delete_lead(self, lead_id: int) -> bool:
        lead = await self.get_lead_by_id(lead_id)
        if lead:
            await self.session.delete(lead)
            await self.session.commit()
            return True
        return False

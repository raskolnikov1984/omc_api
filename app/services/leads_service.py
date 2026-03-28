from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import LeadSQL
from app.schemes.leads import LeadScheme, LeadUpdateScheme


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

    async def update_lead(
        self, lead_id: int, data: LeadUpdateScheme
    ) -> Optional[LeadSQL]:
        lead = await self.get_lead_by_id(lead_id)
        if not lead:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(lead, field, value)

        await self.session.commit()
        await self.session.refresh(lead)
        return lead

    async def delete_lead(self, lead_id: int) -> bool:
        lead = await self.get_lead_by_id(lead_id)
        if lead:
            await self.session.delete(lead)
            await self.session.commit()
            return True
        return False

    async def get_stats(self) -> dict:
        # Total de leads
        total_result = await self.session.execute(select(func.count(LeadSQL.id)))
        total_leads = total_result.scalar() or 0

        # Leads por fuente
        source_result = await self.session.execute(
            select(LeadSQL.source, func.count(LeadSQL.id)).group_by(LeadSQL.source)
        )
        leads_by_source = {row[0]: row[1] for row in source_result.all()}

        # Promedio de presupuesto
        avg_result = await self.session.execute(select(func.avg(LeadSQL.budget)))
        average_budget = avg_result.scalar()

        # Leads últimos 7 días
        seven_days_ago = datetime.now() - timedelta(days=7)
        last_7_days_result = await self.session.execute(
            select(func.count(LeadSQL.id)).where(LeadSQL.created_at >= seven_days_ago)
        )
        leads_last_7_days = last_7_days_result.scalar() or 0

        return {
            "total_leads": total_leads,
            "leads_by_source": leads_by_source,
            "average_budget": average_budget,
            "leads_last_7_days": leads_last_7_days,
        }

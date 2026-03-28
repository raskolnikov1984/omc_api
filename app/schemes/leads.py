from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class LeadScheme(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    phone: str | None = None
    source: Literal[
        "instagram",
        "facebook",
        "landing_page",
        "referido",
        "otro",
    ]
    target_product: str | None = None
    budget: float | None = None
    created_at: datetime | None = None


class LeadUpdateScheme(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    source: (
        Literal[
            "instagram",
            "facebook",
            "landing_page",
            "referido",
            "otro",
        ]
        | None
    ) = None
    target_product: str | None = None
    budget: float | None = None


class LeadStatsScheme(BaseModel):
    total_leads: int
    leads_by_source: dict[str, int]
    average_budget: float | None
    leads_last_7_days: int

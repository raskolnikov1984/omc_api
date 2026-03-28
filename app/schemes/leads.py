from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr


class LeadScheme(BaseModel):
    name: str
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

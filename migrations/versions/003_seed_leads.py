"""seed leads data

Revision ID: 003
Revises: 002
Create Date: 2026-03-28

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    result = op.get_bind().execute(sa.text("SELECT COUNT(*) FROM leads"))
    count = result.scalar()

    if count == 0:
        leads = [
            {
                "name": "Juan Pérez",
                "email": "juan@example.com",
                "phone": "+1234567890",
                "source": "instagram",
                "target_product": "Producto A",
                "budget": 1000.0,
            },
            {
                "name": "María García",
                "email": "maria@example.com",
                "phone": "+1234567891",
                "source": "facebook",
                "target_product": "Producto B",
                "budget": 2000.0,
            },
            {
                "name": "Carlos López",
                "email": "carlos@example.com",
                "phone": "+1234567892",
                "source": "landing_page",
                "target_product": "Producto C",
                "budget": 1500.0,
            },
            {
                "name": "Ana Martínez",
                "email": "ana@example.com",
                "phone": "+1234567893",
                "source": "referido",
                "target_product": "Producto A",
                "budget": 800.0,
            },
            {
                "name": "Pedro Sánchez",
                "email": "pedro@example.com",
                "phone": "+1234567894",
                "source": "otro",
                "target_product": "Producto D",
                "budget": 2500.0,
            },
            {
                "name": "Laura Rodríguez",
                "email": "laura@example.com",
                "phone": "+1234567895",
                "source": "instagram",
                "target_product": "Producto B",
                "budget": 1800.0,
            },
            {
                "name": "Miguel Torres",
                "email": "miguel@example.com",
                "phone": "+1234567896",
                "source": "facebook",
                "target_product": "Producto C",
                "budget": 1200.0,
            },
            {
                "name": "Sofia Hernández",
                "email": "sofia@example.com",
                "phone": "+1234567897",
                "source": "landing_page",
                "target_product": "Producto A",
                "budget": 3000.0,
            },
            {
                "name": "Diego Gómez",
                "email": "diego@example.com",
                "phone": "+1234567898",
                "source": "referido",
                "target_product": "Producto D",
                "budget": 900.0,
            },
            {
                "name": "Isabel Díaz",
                "email": "isabel@example.com",
                "phone": "+1234567899",
                "source": "instagram",
                "target_product": "Producto B",
                "budget": 2200.0,
            },
        ]

        for lead in leads:
            op.execute(
                sa.text(
                    """
                    INSERT INTO leads (name, email, phone, source, target_product, budget, created_at)
                    VALUES (:name, :email, :phone, :source, :target_product, :budget, NOW())
                """
                ),
                lead,
            )


def downgrade() -> None:
    op.execute(sa.text("DELETE FROM leads WHERE email LIKE '%@example.com'"))

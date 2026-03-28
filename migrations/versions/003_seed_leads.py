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
        op.execute(
            sa.text(
                """
                INSERT INTO leads (name, email, phone, source, target_product, budget, created_at) VALUES
                ('Juan Pérez', 'juan@example.com', '+1234567890', 'instagram', 'Producto A', 1000.0, NOW()),
                ('María García', 'maria@example.com', '+1234567891', 'facebook', 'Producto B', 2000.0, NOW()),
                ('Carlos López', 'carlos@example.com', '+1234567892', 'landing_page', 'Producto C', 1500.0, NOW()),
                ('Ana Martínez', 'ana@example.com', '+1234567893', 'referido', 'Producto A', 800.0, NOW()),
                ('Pedro Sánchez', 'pedro@example.com', '+1234567894', 'otro', 'Producto D', 2500.0, NOW()),
                ('Laura Rodríguez', 'laura@example.com', '+1234567895', 'instagram', 'Producto B', 1800.0, NOW()),
                ('Miguel Torres', 'miguel@example.com', '+1234567896', 'facebook', 'Producto C', 1200.0, NOW()),
                ('Sofia Hernández', 'sofia@example.com', '+1234567897', 'landing_page', 'Producto A', 3000.0, NOW()),
                ('Diego Gómez', 'diego@example.com', '+1234567898', 'referido', 'Producto D', 900.0, NOW()),
                ('Isabel Díaz', 'isabel@example.com', '+1234567899', 'instagram', 'Producto B', 2200.0, NOW())
                """
            )
        )


def downgrade() -> None:
    op.execute(sa.text("DELETE FROM leads WHERE email LIKE '%@example.com'"))

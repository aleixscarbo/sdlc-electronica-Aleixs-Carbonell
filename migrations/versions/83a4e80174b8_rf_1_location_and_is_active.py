"""RF-1 location and is_active

Revision ID: 83a4e80174b8
Revises: f6a9e84a9e15
Create Date: 2026-08-20 21:40:49.012641

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "83a4e80174b8"
down_revision: str | Sequence[str] | None = "f6a9e84a9e15"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "sensors",
        sa.Column(
            "location",
            sa.String(length=100),
            server_default="Desconocida",
            nullable=False,
        ),
    )
    op.add_column(
        "sensors",
        sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False),
    )
    op.add_column(
        "alerts",
        sa.Column(
            "status", sa.String(length=20), server_default="open", nullable=False
        ),
    )


def downgrade() -> None:
    op.drop_column("alerts", "status")
    op.drop_column("sensors", "is_active")
    op.drop_column("sensors", "location")

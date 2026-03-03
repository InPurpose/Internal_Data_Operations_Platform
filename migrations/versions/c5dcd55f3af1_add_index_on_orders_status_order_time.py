"""add index on orders(status, order_time)

Revision ID: c5dcd55f3af1
Revises: 445eab7d64b5
Create Date: 2026-02-23 17:31:27.056353

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c5dcd55f3af1'
down_revision: Union[str, Sequence[str], None] = '445eab7d64b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index(
        "idx_orders_status_time",
        "orders",
        ["status", "order_time"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        "idx_orders_status_time",
        table_name="orders"
    )

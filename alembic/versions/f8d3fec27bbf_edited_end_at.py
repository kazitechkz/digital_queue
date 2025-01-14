"""Edited end_at

Revision ID: f8d3fec27bbf
Revises: d0321d354675
Create Date: 2025-01-09 12:14:30.342841

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f8d3fec27bbf"
down_revision: Union[str, None] = "d0321d354675"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "orders", "end_at", existing_type=postgresql.TIMESTAMP(), nullable=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "orders", "end_at", existing_type=postgresql.TIMESTAMP(), nullable=False
    )
    # ### end Alembic commands ###

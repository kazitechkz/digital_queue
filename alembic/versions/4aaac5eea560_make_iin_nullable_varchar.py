"""Make iin nullable varchar

Revision ID: 4aaac5eea560
Revises: 01fae65cb8b9
Create Date: 2025-01-05 13:28:12.994125

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4aaac5eea560"
down_revision: Union[str, None] = "01fae65cb8b9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users",
        "iin",
        existing_type=sa.VARCHAR(length=12),
        type_=sa.String(length=256),
        nullable=True,
    )
    op.drop_index("ix_users_iin", table_name="users")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index("ix_users_iin", "users", ["iin"], unique=True)
    op.alter_column(
        "users",
        "iin",
        existing_type=sa.String(length=256),
        type_=sa.VARCHAR(length=12),
        nullable=False,
    )
    # ### end Alembic commands ###
"""Added is_verified and status to Organization and Vehicle

Revision ID: 2064488f7fa7
Revises: 4aaac5eea560
Create Date: 2025-01-08 10:54:32.281214

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2064488f7fa7'
down_revision: Union[str, None] = '4aaac5eea560'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('organizations', sa.Column('is_verified', sa.Boolean(), nullable=True))
    op.add_column('vehicles', sa.Column('is_verified', sa.Boolean(), nullable=True))
    op.add_column('vehicles', sa.Column('status', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vehicles', 'status')
    op.drop_column('vehicles', 'is_verified')
    op.drop_column('organizations', 'is_verified')
    # ### end Alembic commands ###
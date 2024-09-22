"""habittrackings_edit

Revision ID: 711e336d4cb0
Revises: e5c7aae3ebf7
Create Date: 2024-09-22 20:47:23.521753

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import column


# revision identifiers, used by Alembic.
revision: str = '711e336d4cb0'
down_revision: Union[str, None] = 'e5c7aae3ebf7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_check_constraint(
        "ck_count_limit",
        "habittrackings",
        column('count') <= 20,
        postgresql_not_valid=True,  # ⬅
    )


def downgrade() -> None:
    op.drop_constraint("ck_count_limit", "habittrackings")


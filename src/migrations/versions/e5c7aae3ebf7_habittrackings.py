"""habittrackings

Revision ID: e5c7aae3ebf7
Revises: f70040ded0cf
Create Date: 2024-09-22 20:41:56.120288

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e5c7aae3ebf7"
down_revision: Union[str, None] = "f70040ded0cf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "habittrackings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("alert_time", sa.DateTime(), nullable=True),
        sa.Column("count", sa.Integer(), nullable=True),
        sa.Column("habit_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["habit_id"], ["habits.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("habittrackings")
    # ### end Alembic commands ###

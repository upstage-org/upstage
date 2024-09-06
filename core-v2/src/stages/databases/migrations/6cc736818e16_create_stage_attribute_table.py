"""Create Stage Attribute Table

Revision ID: 6cc736818e16
Revises: 98f5785608b2
Create Date: 2024-09-06 15:40:46.539297

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6cc736818e16"
down_revision: Union[str, None] = "98f5785608b2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "stage_attribute",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("stage_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), default=None),
        sa.Column(
            "created_on",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("(now() at time zone 'utc')"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["stage_id"], ["stage.id"]),
    )


def downgrade() -> None:
    op.drop_table("stage_attribute")

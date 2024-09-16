"""Create Performance Table

Revision ID: afd989efd05e
Revises: b9108ae6f9cd
Create Date: 2024-09-16 20:13:29.295799

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "afd989efd05e"
down_revision: Union[str, None] = "b9108ae6f9cd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "performance",
        sa.Column(
            "id", sa.BigInteger, primary_key=True, autoincrement=True, nullable=False
        ),
        sa.Column("name", sa.Text, nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("stage_id", sa.Integer, nullable=False),
        sa.Column(
            "created_on",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("(now() at time zone 'utc')"),
        ),
        sa.Column("saved_on", sa.TIMESTAMP(timezone=True), server_default=None),
        sa.Column(
            "recording", sa.Boolean, nullable=False, server_default=sa.text("false")
        ),
        sa.ForeignKeyConstraint(["stage_id"], ["stage.id"]),
    )


def downgrade() -> None:
    op.drop_table("performance")

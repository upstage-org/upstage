"""Create Receive Stat Table

Revision ID: 9baa252d9e11
Revises: abb4760d0c6c
Create Date: 2024-10-01 21:06:47.333892

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9baa252d9e11"
down_revision: Union[str, None] = "abb4760d0c6c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "connection_stats",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("connected_id", sa.String, index=True),
        sa.Column("mqtt_timestamp", sa.DateTime, index=True),
        sa.Column("topic", sa.String),
        sa.Column("payload", sa.JSON),
        sa.Column("created", sa.DateTime, default=sa.func.now(), index=True),
    )


def downgrade() -> None:
    op.drop_table("connection_stats")

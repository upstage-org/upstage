"""Create Connection Stat Table

Revision ID: abb4760d0c6c
Revises: b8c702f9160c
Create Date: 2024-10-01 21:06:47.146823

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "abb4760d0c6c"
down_revision: Union[str, None] = "b8c702f9160c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "receive_stats",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("received_id", sa.String, index=True),
        sa.Column("mqtt_timestamp", sa.DateTime, index=True),
        sa.Column("topic", sa.String),
        sa.Column("payload", sa.JSON),
        sa.Column("created", sa.DateTime, default=sa.func.now(), index=True),
    )


def downgrade() -> None:
    op.drop_table("receive_stats")

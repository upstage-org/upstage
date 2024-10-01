"""Create Performance MQTT Config Table

Revision ID: b8c702f9160c
Revises: f2ac3b0f2098
Create Date: 2024-09-16 20:13:29.967755

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b8c702f9160c"
down_revision: Union[str, None] = "f2ac3b0f2098"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "live_performance_mqtt_config",
        sa.Column(
            "id", sa.BigInteger, primary_key=True, autoincrement=True, nullable=False
        ),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("owner_id", sa.Integer, nullable=False, server_default="0"),
        sa.Column("ip_address", sa.Text, nullable=False),
        sa.Column("websocket_port", sa.Integer, nullable=False, server_default="0"),
        sa.Column("webclient_port", sa.Integer, nullable=False, server_default="0"),
        sa.Column("topic_name", sa.Text, nullable=False, unique=True),
        sa.Column("username", sa.Text, nullable=False),
        sa.Column("password", sa.Text, nullable=False),
        sa.Column(
            "created_on",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("(now() at time zone 'utc')"),
        ),
        sa.Column(
            "expires_on",
            sa.TIMESTAMP(timezone=True),
            nullable=True,
            server_default=None,
        ),
        sa.Column("performance_id", sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(["performance_id"], ["performance.id"]),
        sa.ForeignKeyConstraint(["owner_id"], ["upstage_user.id"]),
    )


def downgrade() -> None:
    op.drop_table("live_performance_mqtt_config")

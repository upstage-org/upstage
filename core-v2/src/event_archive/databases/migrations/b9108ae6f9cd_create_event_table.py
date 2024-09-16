"""Create Event Table

Revision ID: b9108ae6f9cd
Revises: df77d2e403eb
Create Date: 2024-09-16 19:54:40.888164

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b9108ae6f9cd"
down_revision: Union[str, None] = "df77d2e403eb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "CREATE SEQUENCE events_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;"
    )

    op.create_table(
        "events",
        sa.Column(
            "id",
            sa.Integer,
            server_default=sa.text("nextval('events_id_seq')"),
            nullable=False,
        ),
        sa.Column("performance_id", sa.Integer),
        sa.Column("topic", sa.Text, nullable=False),
        sa.Column("mqtt_timestamp", sa.Float, nullable=False),
        sa.Column(
            "created",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("payload", sa.JSON, nullable=False),
        sa.PrimaryKeyConstraint("id", name="events_id"),
    )

    op.create_index("events_created", "events", ["created"], unique=False)
    op.create_index("events_performance_id", "events", ["performance_id"], unique=False)


def downgrade() -> None:
    op.drop_index("events_performance_id", table_name="events")
    op.drop_index("events_created", table_name="events")
    op.drop_table("events")
    op.execute("DROP SEQUENCE IF EXISTS events_id_seq;")

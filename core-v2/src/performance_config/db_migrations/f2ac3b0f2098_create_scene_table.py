"""Create Scene Table

Revision ID: f2ac3b0f2098
Revises: 40d8412b181e
Create Date: 2024-09-16 20:13:29.741688

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f2ac3b0f2098"
down_revision: Union[str, None] = "40d8412b181e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "scene",
        sa.Column(
            "id", sa.BigInteger, primary_key=True, autoincrement=True, nullable=False
        ),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("scene_order", sa.Integer, nullable=False, server_default="0"),
        sa.Column("scene_preview", sa.Text, nullable=True),
        sa.Column("payload", sa.Text, nullable=False),
        sa.Column(
            "created_on",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("(now() at time zone 'utc')"),
        ),
        sa.Column("active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("owner_id", sa.Integer, nullable=False, server_default="0"),
        sa.Column("stage_id", sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(["stage_id"], ["stage.id"]),
        sa.ForeignKeyConstraint(["owner_id"], ["upstage_user.id"]),
    )

    op.create_index(
        "scene_scene_order_idx",
        "scene",
        ["scene_order"],
        unique=False,
        postgresql_using="btree",
    )


def downgrade() -> None:
    op.drop_index("scene_scene_order_idx", table_name="scene")
    op.drop_table("scene")

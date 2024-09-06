"""Create Asset Usage Table

Revision ID: 81d1e2707861
Revises: bd3e932ce57a
Create Date: 2024-09-06 15:22:43.175006

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "81d1e2707861"
down_revision: Union[str, None] = "bd3e932ce57a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "asset_usage",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("approved", sa.Boolean(), nullable=False, default=False),
        sa.Column("seen", sa.Boolean(), nullable=False, default=False),
        sa.Column("note", sa.Text()),
        sa.Column(
            "created_on",
            sa.TIMESTAMP(),
            server_default=sa.text("(now() at time zone 'utc')"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["asset_id"],
            ["asset.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["upstage_user.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("asset_usage")

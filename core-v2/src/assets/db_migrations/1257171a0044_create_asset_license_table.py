"""Create Asset License Table

Revision ID: 1257171a0044
Revises: 498a7e2ade05
Create Date: 2024-09-06 15:22:42.804723

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1257171a0044"
down_revision: Union[str, None] = "498a7e2ade05"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "asset_license",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_on",
            sa.TIMESTAMP(),
            server_default=sa.text("(now() at time zone 'utc')"),
        ),
        sa.Column("level", sa.Integer(), nullable=False),
        sa.Column("permissions", sa.TEXT()),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["asset_id"],
            ["asset.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("asset_license")

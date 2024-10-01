"""Create Asset Atribute Table

Revision ID: bd3e932ce57a
Revises: 1257171a0044
Create Date: 2024-09-06 15:22:42.988024

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bd3e932ce57a"
down_revision: Union[str, None] = "1257171a0044"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "asset_attribute",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), default=None),
        sa.Column(
            "created_on",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("(now() at time zone 'utc')"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["asset_id"], ["asset.id"]),
    )


def downgrade() -> None:
    op.drop_table("asset_attribute")

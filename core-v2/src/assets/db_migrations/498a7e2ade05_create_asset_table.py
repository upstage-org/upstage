"""Create Asset Table

Revision ID: 498a7e2ade05
Revises: 228da801fb0c
Create Date: 2024-09-06 15:22:42.623091

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "498a7e2ade05"
down_revision: Union[str, None] = "228da801fb0c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "asset",
        sa.Column("id", sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("asset_type_id", sa.Integer(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), default=None),
        sa.Column("file_location", sa.Text(), nullable=False),
        sa.Column("copyright_level", sa.Integer(), nullable=False, default=0),
        sa.Column(
            "created_on",
            sa.TIMESTAMP(),
            server_default=sa.text("(now() at time zone 'utc')"),
        ),
        sa.Column(
            "updated_on",
            sa.TIMESTAMP(),
            server_default=sa.text("(now() at time zone 'utc')"),
        ),
        sa.Column("size", sa.BigInteger(), nullable=False, default=0),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["asset_type_id"], ["asset_type.id"]),
        sa.ForeignKeyConstraint(["owner_id"], ["upstage_user.id"]),
    )


def downgrade() -> None:
    op.drop_table("asset")

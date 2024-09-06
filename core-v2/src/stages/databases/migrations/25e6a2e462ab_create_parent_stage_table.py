"""Create Parent Stage Table

Revision ID: 25e6a2e462ab
Revises: 6cc736818e16
Create Date: 2024-09-06 15:40:46.723483

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "25e6a2e462ab"
down_revision: Union[str, None] = "6cc736818e16"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "parent_stage",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("stage_id", sa.Integer(), nullable=False),
        sa.Column("child_asset_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["stage_id"], ["stage.id"]),
        sa.ForeignKeyConstraint(["child_asset_id"], ["asset.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("parent_stage")

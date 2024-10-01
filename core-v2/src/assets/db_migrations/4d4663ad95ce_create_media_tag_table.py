"""Create Media Tag Table

Revision ID: 4d4663ad95ce
Revises: 81d1e2707861
Create Date: 2024-09-06 15:22:43.357377

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4d4663ad95ce"
down_revision: Union[str, None] = "81d1e2707861"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "media_tag",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_on",
            sa.TIMESTAMP(),
            server_default=sa.text("(now() at time zone 'utc')"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["asset_id"], ["asset.id"]),
        sa.ForeignKeyConstraint(["tag_id"], ["tag.id"]),
    )


def downgrade() -> None:
    op.drop_table("media_tag")

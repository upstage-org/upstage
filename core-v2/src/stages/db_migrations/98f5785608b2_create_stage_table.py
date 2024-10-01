"""Create Stage Table

Revision ID: 98f5785608b2
Revises: 4d4663ad95ce
Create Date: 2024-09-06 15:40:46.347784

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "98f5785608b2"
down_revision: Union[str, None] = "4d4663ad95ce"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "stage",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), default=None),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("file_location", sa.String(), nullable=False),
        sa.Column(
            "created_on",
            sa.TIMESTAMP(),
            server_default=sa.text("(now() at time zone 'utc')"),
        ),
        sa.Column("last_access", sa.TIMESTAMP(timezone=False)),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["owner_id"], ["upstage_user.id"]),
    )


def downgrade() -> None:
    op.drop_table("stage")

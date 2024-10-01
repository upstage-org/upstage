"""Create Tag Table

Revision ID: c37d2e3ebe8f
Revises: f47aa2b149ba
Create Date: 2024-09-06 15:22:42.250779

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c37d2e3ebe8f"
down_revision: Union[str, None] = "f47aa2b149ba"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tag",
        sa.Column("id", sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("color", sa.Text(), default=None),
        sa.Column(
            "created_on",
            sa.TIMESTAMP(),
            server_default=sa.text("(now() at time zone 'utc')"),
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("tag")

"""Create Jwt No List Table

Revision ID: 175238bc5a72
Revises: 52b22654c1fc
Create Date: 2024-09-02 21:55:00.718580

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "175238bc5a72"
down_revision: Union[str, None] = "52b22654c1fc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "jwt_no_list",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("token", sa.Text(), nullable=False, unique=True),
        sa.Column("token_type", sa.Text(), nullable=False),
        sa.Column(
            "remove_after",
            sa.TIMESTAMP(timezone=False),
            server_default=sa.text("(now() at time zone 'utc')"),
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("jwt_no_list")

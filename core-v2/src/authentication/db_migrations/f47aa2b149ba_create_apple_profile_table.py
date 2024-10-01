"""Create Apple Profile Table

Revision ID: f47aa2b149ba
Revises: b62774b03457
Create Date: 2024-09-02 21:58:12.681615

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f47aa2b149ba"
down_revision: Union[str, None] = "b62774b03457"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "apple_profile",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("apple_id", sa.Text(), nullable=False, server_default=""),
        sa.Column("apple_phone", sa.Text(), nullable=True),
        sa.Column("apple_email", sa.Text(), nullable=True),
        sa.Column("apple_first_name", sa.Text(), nullable=True),
        sa.Column("apple_last_name", sa.Text(), nullable=True),
        sa.Column("apple_username", sa.Text(), nullable=True),
        sa.Column("other_profile_json", sa.Text(), nullable=True),
        sa.Column(
            "received_datetime",
            sa.TIMESTAMP(timezone=True),
            nullable=True,
            server_default=sa.text("(now() at time zone 'utc')"),
        ),
        sa.ForeignKeyConstraint(["user_id"], ["upstage_user.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("apple_profile")

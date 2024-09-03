"""Create Google Profile Table

Revision ID: 88819120e127
Revises: 175238bc5a72
Create Date: 2024-09-02 21:56:55.103267

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "88819120e127"
down_revision: Union[str, None] = "175238bc5a72"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "google_profile",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("google_id", sa.Text(), nullable=False, server_default=""),
        sa.Column("google_phone", sa.Text(), nullable=True),
        sa.Column("google_email", sa.Text(), nullable=True),
        sa.Column("google_first_name", sa.Text(), nullable=True),
        sa.Column("google_last_name", sa.Text(), nullable=True),
        sa.Column("google_username", sa.Text(), nullable=True),
        sa.Column("other_profile_json", sa.Text(), nullable=True),
        sa.Column(
            "received_datetime",
            sa.TIMESTAMP(timezone=True),
            nullable=True,
            server_default=sa.text("(now() at time zone 'utc')"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["upstage_user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("google_profile")

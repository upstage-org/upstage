"""Create User Session Table

Revision ID: 52b22654c1fc
Revises: e2bb50b52d40
Create Date: 2024-09-02 21:46:07.205609

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "52b22654c1fc"
down_revision: Union[str, None] = "e2bb50b52d40"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_session",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("access_token", sa.Text(), nullable=False, default=""),
        sa.Column("refresh_token", sa.Text(), nullable=False, default=""),
        sa.Column(
            "recorded_time",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("(now() at time zone 'utc')"),
        ),
        sa.Column("app_version", sa.Text(), nullable=True),
        sa.Column("app_os_type", sa.Text(), nullable=True),
        sa.Column("app_os_version", sa.Text(), nullable=True),
        sa.Column("app_device", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"], ["upstage_user.id"], deferrable=True, initially="DEFERRED"
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("user_session")

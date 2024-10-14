"""Create One Time OTP

Revision ID: c5c56a2bfa78
Revises: 9baa252d9e11
Create Date: 2024-10-12 12:59:33.781010

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c5c56a2bfa78"
down_revision: Union[str, None] = "9baa252d9e11"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "admin_one_time_totp_qr_url",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("upstage_user.id"),
            unique=True,
            nullable=False,
            default=0,
        ),
        sa.Column("url", sa.Text, nullable=False, default=""),
        sa.Column("code", sa.Text, nullable=False, default=""),
        sa.Column(
            "recorded_time",
            sa.DateTime,
            nullable=False,
            index=True,
            default=sa.func.now(),
        ),
        sa.Column("active", sa.Boolean, nullable=False, index=True, default=True),
    )


def downgrade() -> None:
    op.drop_table("admin_one_time_totp_qr_url")

"""Create Performance Config Table

Revision ID: 40d8412b181e
Revises: afd989efd05e
Create Date: 2024-09-16 20:13:29.533326

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "40d8412b181e"
down_revision: Union[str, None] = "afd989efd05e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "performance_config",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column(
            "owner_id",
            sa.Integer,
            sa.ForeignKey("upstage_user.id"),
            nullable=False,
            default=0,
        ),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("splash_screen_text", sa.Text, nullable=True, default=None),
        sa.Column("splash_screen_animation_urls", sa.Text, nullable=True, default=None),
        sa.Column("created_on", sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column("expires_on", sa.DateTime, nullable=False, default=None),
    )


def downgrade() -> None:
    op.drop_table("performance_config")

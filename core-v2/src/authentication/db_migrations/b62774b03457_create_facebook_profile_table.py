"""Create Facebook Profile Table

Revision ID: b62774b03457
Revises: 88819120e127
Create Date: 2024-09-02 21:58:12.491806

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b62774b03457"
down_revision: Union[str, None] = "88819120e127"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "facebook_profile",
        sa.Column("id", sa.BIGINT(), nullable=False),
        sa.Column("user_id", sa.INTEGER(), nullable=True),
        sa.Column("facebook_id", sa.TEXT(), nullable=False, server_default=""),
        sa.Column("facebook_phone", sa.TEXT(), nullable=True),
        sa.Column("facebook_email", sa.TEXT(), nullable=True),
        sa.Column("facebook_first_name", sa.TEXT(), nullable=True),
        sa.Column("facebook_last_name", sa.TEXT(), nullable=True),
        sa.Column("facebook_username", sa.TEXT(), nullable=True),
        sa.Column("other_profile_json", sa.TEXT(), nullable=True),
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
    op.drop_table("facebook_profile")

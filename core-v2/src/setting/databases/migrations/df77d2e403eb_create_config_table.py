"""Create Config Table

Revision ID: df77d2e403eb
Revises: 25e6a2e462ab
Create Date: 2024-09-06 20:01:55.098610

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "df77d2e403eb"
down_revision: Union[str, None] = "25e6a2e462ab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "config",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("value", sa.Text(), nullable=True, default=None),
        sa.Column(
            "created_on",
            sa.TIMESTAMP(),
            server_default=sa.text("(now() at time zone 'utc')"),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.execute(
        """
        -- Seed foyer config
        INSERT INTO "config" ("name", "value") VALUES ('FOYER_TITLE', 'CYBERFORMANCE PLATFORM');
        INSERT INTO "config" ("name", "value") VALUES ('FOYER_DESCRIPTION', 'UpStage is an online venue for live performance: remote performers collaborate in real time using digital media, and online audiences anywhere in the world join events by going to a web page, without having to download and install any additional software. UpStage is available free to anyone who would like to use it.');
        INSERT INTO "config" ("name", "value") VALUES ('FOYER_MENU', 'UpStage User Manual (https://docs.upstage.live/)
        Customise Foyer (/studio/legacy/backstage/admin/foyer-customisation) (8,32)');

        INSERT INTO "config" ("name", "value") VALUES ('ENABLE_DONATE', 'true');
        """
    )


def downgrade() -> None:
    op.drop_table("config")

"""Create User Table

Revision ID: e2bb50b52d40
Revises: 
Create Date: 2024-08-30 20:33:45.298927

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e2bb50b52d40'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'upstage_user',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('username', sa.Text(), nullable=False, unique=True),
        sa.Column('password', sa.Text(), nullable=False),
        sa.Column('email', sa.Text(), nullable=True, unique=True),
        sa.Column('bin_name', sa.Text(), nullable=False),
        sa.Column('role', sa.Integer(), nullable=False, default=0),
        sa.Column('first_name', sa.Text(), nullable=True),
        sa.Column('last_name', sa.Text(), nullable=True),
        sa.Column('display_name', sa.Text(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False, default=False),
        sa.Column('firebase_pushnot_id', sa.Text(), nullable=True),
        sa.Column('created_on', sa.TIMESTAMP(timezone=True), nullable=True, server_default=sa.text("(now() at time zone 'utc')")),
        sa.Column('deactivated_on', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('upload_limit', sa.Integer(), nullable=True),
        sa.Column('intro', sa.Text(), nullable=True),
        sa.Column('can_send_email', sa.Boolean(), nullable=False, default=False),
        sa.Column('last_login', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('upstage_user')

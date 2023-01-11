"""add user table

Revision ID: 4215baf2e274
Revises: 7295a1c3aaca
Create Date: 2023-01-10 14:04:42.701997

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.sqltypes import TIMESTAMP


# revision identifiers, used by Alembic.
revision = '4215baf2e274'
down_revision = '7295a1c3aaca'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', sa.Column('phone', sa.String(), nullable=False, primary_key=True), 
    sa.Column('name', sa.String(), nullable=True), 
    sa.Column('password', sa.String(), nullable=False), 
    sa.Column('registered_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False), 
    sa.UniqueConstraint('phone'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass


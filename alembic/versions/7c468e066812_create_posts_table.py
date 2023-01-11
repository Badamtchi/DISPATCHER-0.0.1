"""create posts table

Revision ID: 7c468e066812
Revises: 
Create Date: 2023-01-09 21:38:40.284862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c468e066812'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('messages', sa.Column('id', sa.UUID(), nullable=False, primary_key=True)
    , sa.Column('sender', sa.String(), nullable=False), sa.Column('receiver', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('messages')
    pass

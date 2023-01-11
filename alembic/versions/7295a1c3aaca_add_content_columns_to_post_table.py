"""add content columns to post table

Revision ID: 7295a1c3aaca
Revises: 7c468e066812
Create Date: 2023-01-10 13:48:48.225278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7295a1c3aaca'
down_revision = '7c468e066812'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('messages', sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('messages', 'title')
    pass

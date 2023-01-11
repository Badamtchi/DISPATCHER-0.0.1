"""finish tabeles

Revision ID: f691a82755fd
Revises: 4215baf2e274
Create Date: 2023-01-11 07:40:40.456603

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.sqltypes import TIMESTAMP


# revision identifiers, used by Alembic.
revision = 'f691a82755fd'
down_revision = '4215baf2e274'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('messages', sa.Column('seen', sa.Boolean(), nullable=False, server_default='False'))
    op.add_column('messages', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('messages', 'senn')
    op.drop_column('messages', 'created_at')
    pass

"""add content column to posts table

Revision ID: 72e04df8fc8c
Revises: 63acf1995ed4
Create Date: 2026-07-27 14:04:17.855608

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72e04df8fc8c'
down_revision: Union[str, Sequence[str], None] = '63acf1995ed4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
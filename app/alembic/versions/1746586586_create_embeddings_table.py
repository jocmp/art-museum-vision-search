"""Create Embeddings table

Revision ID: ebd15fd7b95b
Revises: 7ffb0cb78794
Create Date: 2025-05-07 02:56:26.360585

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = 'ebd15fd7b95b'
down_revision: Union[str, None] = '7ffb0cb78794'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'embeddings',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('object_id', sa.String(), nullable=False),
        sa.Column('image_url', sa.String(), nullable=False),
        sa.Column('image_vector', Vector(3), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('embeddings')

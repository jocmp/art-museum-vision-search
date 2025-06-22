"""Add embeddings updated_at column

Revision ID: b94dcc76666b
Revises: b2b02fe015d9
Create Date: 2025-06-22 19:07:29.384923

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b94dcc76666b'
down_revision: Union[str, None] = 'b2b02fe015d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('embeddings', sa.Column('updated_at', sa.DateTime(timezone=True)))

def downgrade() -> None:
    op.drop_column('embeddings', 'updated_at')

"""Add L2 embeddings index

Revision ID: b2b02fe015d9
Revises: ebd15fd7b95b
Create Date: 2025-05-09 02:03:45.743736

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'b2b02fe015d9'
down_revision: Union[str, None] = 'ebd15fd7b95b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "CREATE INDEX ON embeddings USING hnsw (image_vector vector_l2_ops)")


def downgrade() -> None:
    pass

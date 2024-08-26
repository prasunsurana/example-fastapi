"""add content column

Revision ID: 12e9166ca883
Revises: d22d2a44c93b
Create Date: 2024-08-26 13:42:06.437008

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12e9166ca883'
down_revision: Union[str, None] = 'd22d2a44c93b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass

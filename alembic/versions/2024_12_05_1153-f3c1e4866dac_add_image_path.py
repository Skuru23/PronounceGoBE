"""add image path

Revision ID: f3c1e4866dac
Revises: 6d3298d40a7b
Create Date: 2024-12-05 11:53:46.772297

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = "f3c1e4866dac"
down_revision: Union[str, None] = "6d3298d40a7b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    op.add_column(
        "groups", sa.Column("image_path", sa.String(length=2048), nullable=True)
    )
    op.add_column(
        "lessons", sa.Column("image_path", sa.String(length=2048), nullable=True)
    )
    op.add_column(
        "users", sa.Column("image_path", sa.String(length=2048), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "image_path")
    op.drop_column("lessons", "image_path")
    op.drop_column("groups", "image_path")
    # ### end Alembic commands ###
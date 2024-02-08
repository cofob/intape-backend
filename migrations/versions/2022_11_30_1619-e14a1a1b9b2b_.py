"""Add metadata_cid to Video.

Revision ID: e14a1a1b9b2b
Revises: 12f1a0a0d114
Create Date: 2022-11-30 16:19:46.186356+00:00
"""
from alembic import op
import sqlalchemy as sa


revision = "e14a1a1b9b2b"
down_revision = "12f1a0a0d114"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("videos", sa.Column("metadata_cid", sa.String(length=128), nullable=True))


def downgrade() -> None:
    op.drop_column("videos", "metadata_cid")

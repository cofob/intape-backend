"""Add tx_hash to Video.

Revision ID: 570a02c3feca
Revises: f8cee6a4cc07
Create Date: 2022-12-01 12:41:45.508059+00:00
"""
from alembic import op
import sqlalchemy as sa


revision = "570a02c3feca"
down_revision = "f8cee6a4cc07"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("videos", sa.Column("tx_hash", sa.String(length=128), nullable=True))


def downgrade() -> None:
    op.drop_column("videos", "tx_hash")

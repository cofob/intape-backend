"""Add is_confirmed column to Video.

Revision ID: f8cee6a4cc07
Revises: e14a1a1b9b2b
Create Date: 2022-11-30 17:16:32.030585+00:00
"""
from alembic import op
import sqlalchemy as sa


revision = "f8cee6a4cc07"
down_revision = "e14a1a1b9b2b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "videos",
        sa.Column("is_confirmed", sa.Boolean(), nullable=False, default=False, server_default=sa.text("false")),
    )


def downgrade() -> None:
    op.drop_column("videos", "is_confirmed")

"""Extend the length of the password column in the users table.

Revision ID: e931fc950542
Revises: 53dce73918f0
Create Date: 2022-11-18 12:33:29.474673+00:00
"""
from alembic import op
import sqlalchemy as sa


revision = "e931fc950542"
down_revision = "53dce73918f0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "users", "password", existing_type=sa.VARCHAR(length=64), type_=sa.String(length=128), existing_nullable=False
    )


def downgrade() -> None:
    op.alter_column(
        "users", "password", existing_type=sa.String(length=128), type_=sa.VARCHAR(length=64), existing_nullable=False
    )

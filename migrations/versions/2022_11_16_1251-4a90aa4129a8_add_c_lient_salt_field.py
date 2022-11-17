"""Add client_salt field

Revision ID: 4a90aa4129a8
Revises: b9db83e7ac00
Create Date: 2022-11-16 12:51:00.893466+00:00
"""
from alembic import op
import sqlalchemy as sa


revision = "4a90aa4129a8"
down_revision = "b9db83e7ac00"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("client_salt", sa.String(length=64), server_default="", nullable=False))


def downgrade() -> None:
    op.drop_column("users", "client_salt")

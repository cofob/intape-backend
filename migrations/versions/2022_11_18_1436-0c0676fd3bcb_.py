"""Add User relation to File model.

Revision ID: 0c0676fd3bcb
Revises: e931fc950542
Create Date: 2022-11-18 14:36:26.147498+00:00
"""
from alembic import op
import sqlalchemy as sa


revision = "0c0676fd3bcb"
down_revision = "e931fc950542"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("DELETE FROM files")
    op.add_column("files", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key(None, "files", "users", ["user_id"], ["id"])


def downgrade() -> None:
    op.drop_constraint(None, "files", type_="foreignkey")
    op.drop_column("files", "user_id")

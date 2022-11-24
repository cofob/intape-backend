"""Add File model.

Revision ID: 53dce73918f0
Revises: 4a90aa4129a8
Create Date: 2022-11-17 14:13:59.748686+00:00
"""
from alembic import op
import sqlalchemy as sa


revision = "53dce73918f0"
down_revision = "4a90aa4129a8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "files",
        sa.Column("cid", sa.String(length=128), nullable=False),
        sa.Column("mime_type", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("remove_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("cid"),
    )
    op.create_index(op.f("ix_files_cid"), "files", ["cid"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_files_cid"), table_name="files")
    op.drop_table("files")

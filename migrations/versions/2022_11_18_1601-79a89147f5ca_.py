"""Add Video model.

Revision ID: 79a89147f5ca
Revises: 0c0676fd3bcb
Create Date: 2022-11-18 16:01:18.424417+00:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "79a89147f5ca"
down_revision = "0c0676fd3bcb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "videos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(length=150), nullable=False),
        sa.Column("tags", postgresql.ARRAY(sa.String(length=16)), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("file_cid", sa.String(length=128), nullable=False),
        sa.ForeignKeyConstraint(
            ["file_cid"],
            ["files.cid"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_videos_id"), "videos", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_videos_id"), table_name="videos")
    op.drop_table("videos")

"""Add UserTokenModel

Revision ID: b9db83e7ac00
Revises: 000000000000
Create Date: 2022-11-16 09:45:06.503664+00:00
"""
from alembic import op
import sqlalchemy as sa


revision = "b9db83e7ac00"
down_revision = "000000000000"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user_tokens",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("iat", sa.Integer(), nullable=False),
        sa.Column("exp", sa.Integer(), nullable=False),
        sa.Column("session_info", sa.String(length=64), nullable=True),
        sa.Column("revoked", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_tokens_id"), "user_tokens", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_user_tokens_id"), table_name="user_tokens")
    op.drop_table("user_tokens")

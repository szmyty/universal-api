"""Create messages table with user_id and timestamps

Revision ID: 0001_create_message_table
Revises:
Create Date: 2025-06-23 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic.
revision = "0001_create_message_table"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create messages table."""
    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, index=True),
        sa.Column("user_id", sa.String(), nullable=False, index=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )


def downgrade() -> None:
    """Drop messages table."""
    op.drop_table("messages")

"""Create map_states table with user_id, name, state and timestamps

Revision ID: 0002_create_map_state_table
Revises: 0001_create_message_table
Create Date: 2025-06-23 12:01:00.000000
"""

from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = "0002_create_map_state_table"
down_revision = "0001_create_message_table"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create map_states table."""
    op.create_table(
        "map_states",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, index=True),
        sa.Column("user_id", sa.String(), nullable=False, index=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("state", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Drop map_states table."""
    op.drop_table("map_states")

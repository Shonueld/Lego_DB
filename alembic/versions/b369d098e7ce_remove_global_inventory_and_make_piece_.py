"""remove global inventory and make piece count nullable

Revision ID: b369d098e7ce
Revises: 78fdef0b9bdb
Create Date: 2025-05-09 21:02:17.810341

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b369d098e7ce'
down_revision: Union[str, None] = '78fdef0b9bdb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Drop the global_inventory table
    op.drop_table("global_inventory")
    
    # Make number_of_parts column nullable
    op.alter_column(
        "sets",
        "number_of_parts",
        existing_type=sa.Integer(),
        nullable=True
    )

def downgrade() -> None:
    # Recreate the global_inventory table
    op.create_table(
        "global_inventory",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("gold", sa.Integer, nullable=False),
        sa.CheckConstraint("gold >= 0", name="check_gold_positive"),
    )

    # Re-insert initial row
    op.execute(sa.text("INSERT INTO global_inventory (gold) VALUES (100)"))

    # Revert number_of_parts column to non-nullable
    op.alter_column(
        "sets",
        "number_of_parts",
        existing_type=sa.Integer(),
        nullable=False
    )
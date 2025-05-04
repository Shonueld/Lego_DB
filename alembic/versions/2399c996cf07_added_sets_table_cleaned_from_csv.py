"""added sets table cleaned from csv

Revision ID: 2399c996cf07
Revises: 70ffb0cef819
Create Date: 2025-05-04 15:46:04.253167

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2399c996cf07'
down_revision: Union[str, None] = '70ffb0cef819'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'sets',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('set_number', sa.String, nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('year_released', sa.Integer, nullable=False),
        sa.Column('number_of_parts', sa.Integer, nullable=False),
        sa.Column('theme_name', sa.String, nullable=False)
    )

def downgrade():
    op.drop_table('sets')

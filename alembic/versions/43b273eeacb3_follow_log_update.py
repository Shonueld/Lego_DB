"""follow log update

Revision ID: 43b273eeacb3
Revises: b7109a447ec1
Create Date: 2025-05-26 16:01:28.376553

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43b273eeacb3'
down_revision: Union[str, None] = 'b7109a447ec1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('follow_log', sa.Column('status', sa.String(), nullable=False, server_default='followed'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('follow_log', 'status')

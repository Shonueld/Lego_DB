"""friends to followers

Revision ID: b7109a447ec1
Revises: e64c9b356c6e
Create Date: 2025-05-26 15:33:26.571156

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7109a447ec1'
down_revision: Union[str, None] = 'e64c9b356c6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table('friends', 'followers')
    op.alter_column('followers', 'friend_id', new_column_name='following_id')

    op.create_table(
        'follow_log',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('following_id', sa.Integer(), nullable=False),
        sa.Column('followed_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id']),
        sa.ForeignKeyConstraint(['following_id'], ['users.user_id'])
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('follow_log')
    op.alter_column('followers', 'following_id', new_column_name='friend_id')
    op.rename_table('followers', 'friends')

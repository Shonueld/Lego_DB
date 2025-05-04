"""added lists, users, and friends table

Revision ID: 78fdef0b9bdb
Revises: 2399c996cf07
Create Date: 2025-05-04 16:29:04.368525

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78fdef0b9bdb'
down_revision: Union[str, None] = '2399c996cf07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "lists",
        sa.Column("list_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.user_id"), nullable=False),
        sa.Column("set_id", sa.Integer, sa.ForeignKey("sets.id"), nullable=False),
        sa.Column("status", sa.String, nullable=False),  # e.g. "completed", "wishlist", "in progress"
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "users",
        sa.Column("user_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("username", sa.String, nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "friends",
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.user_id"), primary_key=True),
        sa.Column("friend_id", sa.Integer, sa.ForeignKey("users.user_id"), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("user_id != friend_id", name="no_self_friendship")
    )
    op.create_table(
        'reviews',
        sa.Column('review_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('set_id', sa.Integer, sa.ForeignKey('sets.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False),
        sa.Column('rating', sa.Integer, nullable=False),
        sa.Column('description', sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        'issues',
        sa.Column('issue_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('set_id', sa.Integer, sa.ForeignKey('sets.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False),
        sa.Column('description', sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("issues")
    op.drop_table("reviews")
    op.drop_table("friends")
    op.drop_table("lists")
    op.drop_table("users")
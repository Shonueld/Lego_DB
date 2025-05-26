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
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

@router.post("/{user_id}/follow", status_code=status.HTTP_200_OK)
def follow_another_user(user_id: int, following: FollowUserRequest):
    with db.engine.begin() as connection:
        # existing follow logic...

        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO follow_log (user_id, following_id, status)
                VALUES (:user_id, :following_id, 'followed')
                """
            ),
            {"user_id": user_id, "following_id": following.following_id},
        )

        # rest of the function...

@router.post("/{user_id}/unfollow", status_code=status.HTTP_200_OK)
def unfollow_user(user_id: int, following: FollowUserRequest):
    with db.engine.begin() as connection:
        # Check if the relationship exists
        exists = connection.execute(
            sqlalchemy.text(
                """
                SELECT 1 FROM followers
                WHERE user_id = :user_id AND following_id = :following_id
                """
            ),
            {"user_id": user_id, "following_id": following.following_id},
        ).scalar_one_or_none()

        if not exists:
            raise HTTPException(status_code=400, detail="Not following this user")

        # Delete the follower relationship
        connection.execute(
            sqlalchemy.text(
                """
                DELETE FROM followers
                WHERE user_id = :user_id AND following_id = :following_id
                """
            ),
            {"user_id": user_id, "following_id": following.following_id},
        )

        # Log the unfollow action
        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO follow_log (user_id, following_id, status)
                VALUES (:user_id, :following_id, 'unfollowed')
                """
            ),
            {"user_id": user_id, "following_id": following.following_id},
        )

        follower_username = connection.execute(
            sqlalchemy.text("SELECT username FROM users WHERE user_id = :user_id"),
            {"user_id": user_id},
        ).scalar_one()

        following_username = connection.execute(
            sqlalchemy.text("SELECT username FROM users WHERE user_id = :following_id"),
            {"following_id": following.following_id},
        ).scalar_one()

    return {"message": f"{follower_username} unfollowed {following_username}"}

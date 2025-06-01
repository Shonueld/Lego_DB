from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
import sqlalchemy
from src.api import auth
from enum import Enum
from typing import List, Optional
from src import database as db


router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(auth.get_api_key)],
)


class NewUser(BaseModel):
    username: str = Field(..., min_length=1)
class FollowUserRequest(BaseModel):
    following_id: int
class UserId(BaseModel):
    user_id: int


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(new_user: NewUser):
    with db.engine.begin() as connection:
    
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT COUNT(*) 
                FROM users 
                WHERE username = :username
                """),
            {"username": new_user.username},
        ).scalar_one()

        if result > 0:
            raise HTTPException(status_code=400, detail="Username already exists")

        user_id = connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO users (username)
                VALUES (:username)
                RETURNING user_id
                """
            ),
            {"username": new_user.username},
        ).scalar_one()

    return {"message": f"User '{new_user.username}' created successfully with id {user_id}"}


@router.post("/{user_id}/follow", status_code=status.HTTP_201_CREATED)
def follow_another_user(user_id: int, following: FollowUserRequest):
    with db.engine.begin() as connection:
        # Verify both users exist
        user_exists = connection.execute(
            sqlalchemy.text(
                """
                SELECT 1 
                FROM users 
                WHERE user_id = :user_id
                """
                ),
            {"user_id": user_id}
        ).scalar_one_or_none()
        if not user_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} does not exist."
            )

        target_exists = connection.execute(
            sqlalchemy.text(
                """
                SELECT 1 
                FROM users 
                WHERE user_id = :following_id
                """
                ),
            {"following_id": following.following_id}
        ).scalar_one_or_none()
        if not target_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {following.following_id} does not exist."
            )

        # Check for duplicate follow
        already = connection.execute(
            sqlalchemy.text(
                """
                SELECT 1 
                FROM followers 
                WHERE user_id = :user_id AND following_id = :following_id
                """
            ),
            {"user_id": user_id, "following_id": following.following_id}
        ).scalar_one_or_none()
        if already:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User {user_id} is already following user {following.following_id}."
            )

        #safe to insert
        connection.execute(
            sqlalchemy.text(
                "INSERT INTO followers (user_id, following_id) VALUES (:user_id, :following_id)"
            ),
            {"user_id": user_id, "following_id": following.following_id},
        )

        connection.execute(
            sqlalchemy.text(
                "INSERT INTO follow_log (user_id, following_id, status) VALUES (:user_id, :following_id, 'followed')"
            ),
            {"user_id": user_id, "following_id": following.following_id},
        )

        # fetch usernames for the success message
        follower_username = connection.execute(
            sqlalchemy.text("SELECT username FROM users WHERE user_id = :user_id"),
            {"user_id": user_id},
        ).scalar_one()
        following_username = connection.execute(
            sqlalchemy.text("SELECT username FROM users WHERE user_id = :following_id"),
            {"following_id": following.following_id},
        ).scalar_one()

    return {"message": f"{follower_username} started following {following_username}"}


@router.post("/{user_id}/unfollow", status_code=status.HTTP_200_OK)
def unfollow_user(user_id: int, following: FollowUserRequest):
    with db.engine.begin() as connection:
        delete_result = connection.execute(
            sqlalchemy.text(
                """
                DELETE FROM followers
                WHERE user_id = :user_id AND following_id = :following_id
                """
            ),
            {"user_id": user_id, "following_id": following.following_id},
        )

        if delete_result.rowcount < 1:
            raise HTTPException(status_code=400, detail="Follow relationship does not exist")

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

@router.get("/{user_id}/following-list", status_code=status.HTTP_200_OK)
def get_following_users(user_id: int):
    with db.engine.begin() as connection:
        username = connection.execute(
            sqlalchemy.text(
                """
                SELECT username
                FROM users
                where user_id = :user_id
                """
            ), {"user_id": user_id}).scalar_one_or_none()
        
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT u.username
                FROM users u
                JOIN followers f ON f.following_id = u.user_id
                WHERE f.user_id = :user_id
                """),
            {"user_id": user_id,},).fetchall()
        
        following = [{"following_username": row.username} for row in result]
    

    if username:
        return {"user": username, "following": following}
    return{"user not found"}

@router.get("/{user_id}/activity/{following_id}", status_code=status.HTTP_200_OK)
def get_user_activity_feed(user_id: int, following_id: int):
    with db.engine.begin() as connection:
        is_following = connection.execute(
            sqlalchemy.text(
                """
                SELECT 1
                FROM followers
                WHERE user_id = :user_id AND following_id = :following_id
                """
            ),
            {
                "user_id": user_id,
                "following_id": following_id
            }
        ).scalar_one_or_none()

        if not is_following:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} is not following user {following_id}."
            )

        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT s.id, s.name, l.status, l.created_at
                FROM lists l
                JOIN sets s ON s.id = l.set_id
                WHERE l.user_id = :following_id
                ORDER BY l.created_at DESC
                LIMIT 5
                """
            ),
            {"following_id": following_id}
        ).fetchall()
        
        result_reviews = connection.execute(
            sqlalchemy.text(
                """
                SELECT s.id, s.name, r.rating, r.description, r.created_at
                FROM reviews r
                JOIN sets s ON s.id = r.set_id
                WHERE r.user_id = :following_id
                ORDER BY r.created_at DESC
                LIMIT 5
                """
            ),
            {"following_id": following_id}
        ).fetchall()

        following_username = connection.execute(
            sqlalchemy.text(
                """
                SELECT username
                FROM users
                WHERE user_id = :following_id
                """
            ),
            {"following_id": following_id}
        ).scalar_one_or_none()

    if not result and not result_reviews:
        return{"message": f"No activity found for user '{following_username}'"}

    activity = [
        {
            "set_id": row.id,
            "set_name": row.name,
            "status": row.status,
            "created_at": row.created_at
        }
        for row in result
    ]

    reviews = [
        {
            "set_id": row.id,
            "set_name": row.name,
            "rating": row.rating,
            "description": row.description,
            "created_at": row.created_at
        }
        for row in result_reviews
    ]

    return {
        "following_username": following_username,
        "activity": activity,
        "reviews": reviews
    } 
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
class Friend(BaseModel):
    friend_id:int


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

@router.post("/{user_id}/friends", status_code=status.HTTP_201_CREATED)
def add_friends(user_id: int, friend:Friend):
    with db.engine.begin() as connection:
    
        result = connection.execute(
            sqlalchemy.text(
                """
                WITH valid_ids AS (
                    SELECT 1
                    FROM users u1, users u2
                    WHERE u1.user_id = :user_id AND u2.user_id = :friend_id
                )
                INSERT INTO friends (user_id, friend_id)
                SELECT :user_id, :friend_id
                FROM valid_ids
                WHERE NOT EXISTS( 
                    SELECT 1 FROM friends WHERE user_id = :user_id AND friend_id = :friend_id
                )
                """),
            {"user_id": user_id,
             "friend_id": friend.friend_id },
        )

        if result.rowcount < 1:
                return {"message": "Invalid ids or attempting to enter duplicates"}

    return {"message": f"User:'{user_id}' added friend {friend.friend_id}"}

@router.get("/{user_id}/friends", status_code=status.HTTP_200_OK)
def get_friends(user_id: int):
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
                JOIN friends f ON f.friend_id = u.user_id
                WHERE f.user_id = :user_id
                """),
            {"user_id": user_id,},).fetchall()
        
        friends = [{"friend_username": row.username} for row in result]
    

    if username:
        return {"user": username, "friends": friends}
    return{"user not found"}

@router.get("/{user_id}/friends/{friend_id}/activity", status_code=status.HTTP_200_OK)
def get_friends(user_id: int, friend_id:int ):
    with db.engine.begin() as connection:



        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT s.id, s.name, l.status, l.created_at, r.rating, r.description
                FROM lists l
                JOIN friends f ON f.friend_id = l.user_id
                JOIN sets s ON s.id = l.set_id
                LEFT JOIN reviews r ON r.user_id = l.user_id AND r.set_id = s.id
                WHERE 
                    f.user_id = :user_id AND 
                    f.friend_id = :friend_id
                ORDER BY l.created_at DESC
                LIMIT 5
                """),
            {"user_id": user_id,"friend_id": friend_id},)
        
        resultReviews = connection.execute(
            sqlalchemy.text(
                """
                SELECT s.id, s.name, r.rating, r.description, r.created_at
                FROM reviews r
                JOIN friends f ON f.friend_id = r.user_id
                JOIN sets s ON s.id = r.set_id
                WHERE 
                    f.user_id = :user_id AND 
                    f.friend_id = :friend_id
                ORDER BY r.created_at DESC
                LIMIT 5
                
                """),
            {"user_id": user_id,"friend_id": friend_id},)

        friend_username = connection.execute(
            sqlalchemy.text(
                """
                SELECT username
                FROM users
                WHERE user_id = :friend_id
                """), {"friend_id": friend_id}).scalar_one_or_none()

    if result.rowcount < 1:
        return{"Not Friends"}

    activity = []
    reviews = []

    for row in result:
        entry = {
            "set_id": row.id,
            "set_name": row.name,
            "status": row.status,
            "created_at": row.created_at
        }

        activity.append(entry)

    for row in resultReviews:
        entry = {
            "set_id": row.id,
            "set_name": row.name,
            "created_at": row.created_at
        }

        if row.rating is not None:
            review_entry = entry.copy()
            review_entry["rating"] = row.rating
            review_entry["description"] = row.description
            reviews.append(review_entry)
            

    return {"friend_username": friend_username, "activity": activity, "reviews": reviews} 


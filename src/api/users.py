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
class NewFriend(BaseModel):
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

        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO users (username)
                VALUES (:username)
                """
            ),
            {"username": new_user.username},
        )
    return {"message": f"User '{new_user.username}' created successfully"}

@router.post("/{user_id}/friends", status_code=status.HTTP_201_CREATED)
def add_friends(user_id: int, friend:NewFriend):
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

@router.get("/{user_id}/friends", status_code=status.HTTP_201_CREATED)
def get_friends(user_id: int):
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT * 
                FROM friends

                """),
            {"user_id": user_id,},
        )
    friends = [{"friend_id" : row.friend_id for row in result}]
        

    return {"user_id": user_id, "friends": friends}

@router.get("/{user_id}/friends/activity", status_code=status.HTTP_201_CREATED)
def get_friends(user_id: int):
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT * 
                FROM friends

                """),
            {"user_id": user_id,},
        )
    friends = [{"friend_id" : row.friend_id for row in result}]
        

    return {"user_id": user_id, "friends": friends}


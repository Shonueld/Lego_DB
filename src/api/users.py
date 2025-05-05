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


@router.post("/users", status_code=status.HTTP_201_CREATED)
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

        if result > 1:
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

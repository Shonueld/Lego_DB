from dataclasses import dataclass
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field, field_validator
from typing import List

import sqlalchemy
from src.api import auth
from src import database as db
import random
from datetime import datetime

router = APIRouter(
    prefix="",
    tags=["issues"],
    dependencies=[Depends(auth.get_api_key)],
)

class IssueResponse(BaseModel):
    issue_id: int
    set_id: int
    username: str
    description: str
    created_at: datetime  

@router.post("/sets/{set_id}/issues", status_code=status.HTTP_204_NO_CONTENT)
def post_deliver_bottles(message: str, set_id: int, user_id: int):
   """
   Delivery of potions requested after plan. order_id is a unique value representing
   a single delivery; the call is idempotent based on the order_id.
   """
   print(f"(POST set issuse) message: {message} order_id: {set_id} user_id: {user_id}")


   with db.engine.begin() as connection:
       connection.execute(sqlalchemy.text(
           """
           INSERT INTO issues (set_id, user_id, description)
           VALUES (:set_id, :user_id, :message)
           """
       ),
           {"set_id": set_id,
           "user_id": user_id,
           "message": message}
       )

@router.get("/sets/{set_id}/issues", response_model=List[IssueResponse])
def get_issues_for_set(set_id: int):
    """
    Retrieve all issues reported for a specific set.
    """
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT i.issue_id, i.set_id, u.username, i.description, i.created_at
                FROM issues i
                JOIN users u ON i.user_id = u.user_id
                WHERE i.set_id = :set_id
                ORDER BY i.created_at DESC
                """
            ),
            {"set_id": set_id}
        )
        issues = result.fetchall()

    return [dict(row._mapping) for row in issues]


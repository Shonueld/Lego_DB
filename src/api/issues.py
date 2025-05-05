from dataclasses import dataclass
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

import sqlalchemy
from src.api import auth
from src import database as db

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

class IssueRequest(BaseModel):
    user_id: int
    message: str

@router.post("/sets/{set_id}/issues", status_code=status.HTTP_201_CREATED)
def post_issue(set_id: int, issue: IssueRequest):
    """
    Adds an issue for a specific Lego set.
    """
    with db.engine.begin() as connection:
        # Lookup username for user_id
        user_row = connection.execute(
            sqlalchemy.text("SELECT username FROM users WHERE user_id = :user_id"),
            {"user_id": issue.user_id}
        ).fetchone()

        if not user_row:
            raise HTTPException(status_code=404, detail="User not found.")

        # Insert issue and return new row info
        result = connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO issues (set_id, user_id, description)
                VALUES (:set_id, :user_id, :message)
                RETURNING issue_id, created_at
                """
            ),
            {
                "set_id": set_id,
                "user_id": issue.user_id,
                "message": issue.message
            }
        ).fetchone()

    return {
        "message": "Issue successfully reported.",
        "data": {
            "issue_id": result.issue_id,
            "set_id": set_id,
            "user_id": issue.user_id,
            "username": user_row.username,
            "description": issue.message,
            "created_at": result.created_at
        }
    }

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
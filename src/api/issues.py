from dataclasses import dataclass
from fastapi import APIRouter, Depends, status, HTTPException, Query
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
    message: str = Field(..., min_length=1, description="Issue description must not be empty.")

class IssueMessageResponse(BaseModel):
    message: str
    data: IssueResponse

@router.post("/sets/{set_id}/issues", response_model=IssueMessageResponse, status_code=status.HTTP_201_CREATED)
def post_issue(set_id: int, issue: IssueRequest):
    """
    Adds an issue for a specific Lego set.
    """

    if set_id <= 0:
        raise HTTPException(status_code=400, detail="Set ID must be a positive integer.")
    if issue.user_id <= 0:
        raise HTTPException(status_code=400, detail="User ID must be a positive integer.")
    
    with db.engine.begin() as connection:
        # Lookup username for user_id
        user_row = connection.execute(
            sqlalchemy.text("SELECT username FROM users WHERE user_id = :user_id"),
            {"user_id": issue.user_id}
        ).fetchone()

        if not user_row:
            raise HTTPException(status_code=404, detail="User not found.")

        set_row = connection.execute(
            sqlalchemy.text("SELECT 1 FROM sets WHERE id = :set_id"),
            {"set_id": set_id}
        ).fetchone()

        if not set_row:
            raise HTTPException(status_code=404, detail="Set not found.")

        list_entry = connection.execute(
            sqlalchemy.text("SELECT 1 FROM lists WHERE user_id = :user_id AND set_id = :set_id"),
            {"user_id": issue.user_id, "set_id": set_id}
        ).fetchone()

        if not list_entry:
            raise HTTPException(status_code=400, detail="Set is not in user's list.")

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

    return IssueMessageResponse(
        message="Issue successfully reported.",
        data=IssueResponse(
            issue_id=result.issue_id,
            set_id=set_id,
            username=user_row.username,
            description=issue.message,
            created_at=result.created_at
        )
    )

@router.get("/sets/{set_id}/issues", response_model=List[IssueResponse])
def get_issues_for_set(set_id: int, limit: int = Query(50, ge=1), offset: int = Query(0, ge=0)):
    """
    Retrieve all issues reported for a specific set.
    """

    if set_id <= 0:
        raise HTTPException(status_code=400, detail="Set ID must be a positive integer.")

    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT i.issue_id, i.set_id, u.username, i.description, i.created_at
                FROM issues i
                JOIN users u ON i.user_id = u.user_id
                WHERE i.set_id = :set_id
                ORDER BY i.created_at DESC
                LIMIT :limit OFFSET :offset
                """
            ),
            {"set_id": set_id, "limit": limit, "offset": offset}
        )
        issues = result.fetchall()

    return [
        IssueResponse(
            issue_id=row.issue_id,
            set_id=row.set_id,
            username=row.username,
            description=row.description,
            created_at=row.created_at
        )
        for row in issues
    ]
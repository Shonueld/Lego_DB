from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field
import sqlalchemy
from src import database as db
from src.api import auth
from typing import List, Optional, Dict
from enum import Enum

router = APIRouter(
    prefix="/lists",
    tags=["lists"],
    dependencies=[Depends(auth.get_api_key)],
)

class ListStatusResponse(BaseModel):
    message: str
    username: str
    set_id: int
    status: str

class FollowerActivityResponse(BaseModel):
    follower_username: str
    activity: List[dict]
    reviews: List[dict]

class SetDetailsResponse(BaseModel):
    message: str
    set_details: dict

class ErrorResponse(BaseModel):
    detail: str

class ProgressStatus(BaseModel):
    count: int
    sets: List[str]

class ListProgressResponse(BaseModel):
    message: str
    progress: Dict[str, ProgressStatus]

class ValidStatus(str, Enum):
    wishlist = "wishlist"
    building = "building"
    purchased = "purchased"
    built = "built"

class ListStatusUpdate(BaseModel):
    status: ValidStatus

@router.put("/{user_id}/sets/{set_id}", response_model=ListStatusResponse, status_code=status.HTTP_200_OK)
def update_list_status(user_id: int, set_id: int, body: ListStatusUpdate):
    """
    Updates or inserts a user's status for a specific LEGO set. Valid statuses are: wishlist, building, purchased, built.
    """

    with db.engine.begin() as conn:
        # 1. Get the username
        user = conn.execute(
            sqlalchemy.text(
                """
                SELECT username
                FROM users
                WHERE user_id = :user_id
                """
                ),
            {"user_id": user_id}
        ).fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        username = user.username

        # Check if the set exists
        set_exists = conn.execute(
            sqlalchemy.text(
                """
                SELECT 1
                FROM sets
                WHERE id = :set_id
                """
            ),
            {"set_id": set_id}
        ).scalar_one_or_none()

        if not set_exists:
            raise HTTPException(status_code=404, detail=f"Set with ID {set_id} not found.")


        # 2. Check if the list entry already exists
        existing = conn.execute(
            sqlalchemy.text(
                """
                SELECT list_id, status
                FROM lists
                WHERE user_id = :user_id AND set_id = :set_id
                """
            ),
            {"user_id": user_id, "set_id": set_id}
        ).fetchone()

        if existing:
            current_status = existing.status

            if current_status == body.status:
                return ListStatusResponse(
                    message=f"List entry for set {set_id} already has status '{body.status}'",
                    username=username,
                    set_id=set_id,
                    status=body.status
                )

            # Update existing status
            conn.execute(
                sqlalchemy.text(
                    """
                    UPDATE lists
                    SET status = :status
                    WHERE list_id = :list_id
                    """
                ),
                {"status": body.status, "list_id": existing.list_id}
            )
            action = "updated"
        else:
            # Insert new list entry
            conn.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO lists (user_id, set_id, status)
                    VALUES (:user_id, :set_id, :status)
                    """
                ),
                {"user_id": user_id, "set_id": set_id, "status": body.status}
            )
            action = "created"
    return ListStatusResponse(
        message=f"List entry for set {set_id} has been {action} with status '{body.status}'",
        username=username,
        set_id=set_id,
        status=body.status
    )

# Example Flow 3 - Function 1
@router.get("/{user_id}/progress", response_model=ListProgressResponse, status_code=status.HTTP_200_OK)
def get_list_progress(user_id: int):
    """
    Displays a user's progress for their entire list.
    """

    with db.engine.begin() as conn:
        # 1. Get the username from the user_id
        user = conn.execute(
            sqlalchemy.text(
                """
                SELECT username
                FROM users
                WHERE user_id = :user_id
                """
            ),
            {"user_id": user_id}
        ).fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        username = user.username

        # 2. Get sets grouped by status
        result = conn.execute(
            sqlalchemy.text(
                """
                SELECT l.status, s.name AS set_name
                FROM lists l
                JOIN sets s ON l.set_id = s.id
                WHERE l.user_id = :user_id
                """
            ),
            {"user_id": user_id}
        ).fetchall()

    # 3. Organize results into a dictionary
    progress = {status: {"count": 0, "sets": []} for status in VALID_STATUSES}
    for row in result:
        if row.status in progress:
            progress[row.status]["count"] += 1
            progress[row.status]["sets"].append(row.set_name)

    return ListProgressResponse(
        message=f"Displayed progress for user {username}",
        progress=progress
    )
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field
import sqlalchemy
from src import database as db
from src.api import auth

router = APIRouter(
    prefix="/lists",
    tags=["lists"],
    dependencies=[Depends(auth.get_api_key)],
)

class ListStatusUpdate(BaseModel):
    status: str = Field(..., description="One of: wishlist, building, purchased, built")

VALID_STATUSES = {"wishlist", "purchased", "building", "built"}

@router.put("/{user_id}/sets/{set_id}", status_code=status.HTTP_200_OK)
def update_list_status(user_id: int, set_id: int, body: ListStatusUpdate):
    """
    Updates or inserts a user's status for a specific LEGO set. Valid statuses are: wishlist, building, purchased, built.
    """

    if body.status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid status.")

    with db.engine.begin() as conn:
        # 1. Get the username
        user = conn.execute(
            sqlalchemy.text("""
                SELECT username FROM users WHERE user_id = :user_id
            """),
            {"user_id": user_id}
        ).fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        username = user.username

        # 2. Check if the list entry already exists
        existing = conn.execute(
            sqlalchemy.text("""
                SELECT list_id FROM lists
                WHERE user_id = :user_id AND set_id = :set_id
            """),
            {"user_id": user_id, "set_id": set_id}
        ).fetchone()

        if existing:
            # Update existing status
            conn.execute(
                sqlalchemy.text("""
                    UPDATE lists
                    SET status = :status
                    WHERE list_id = :list_id
                """),
                {"status": body.status, "list_id": existing.list_id}
            )
            action = "updated"
        else:
            # Insert new list entry
            conn.execute(
                sqlalchemy.text("""
                    INSERT INTO lists (user_id, set_id, status)
                    VALUES (:user_id, :set_id, :status)
                """),
                {"user_id": user_id, "set_id": set_id, "status": body.status}
            )
            action = "created"
    return {
        "message": f"List entry for set {set_id} has been {action} with status '{body.status}'",
        "username": username,
        "set_id": set_id,
        "status": body.status
    }

# Example Flow 3 - Function 1
@router.get("/{user_id}/progress", status_code=status.HTTP_200_OK)
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
                ORDER BY l.status, s.name
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

    return {
        "message": f"Displayed progress for user {username}",
        "progress": progress
    }
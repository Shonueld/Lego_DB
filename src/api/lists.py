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

@router.put("/{username}/sets/{set_id}", status_code=status.HTTP_200_OK)
def update_list_status(username: str, set_id: int, body: ListStatusUpdate):
    """
    Updates or inserts a user's status for a specific LEGO set.
    """

    if body.status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid status.")

    with db.engine.begin() as conn:
        # 1. Get the user_id from the username
        user = conn.execute(
            sqlalchemy.text("""
                SELECT user_id FROM users WHERE username = :username
            """),
            {"username": username}
        ).fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        user_id = user.user_id

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
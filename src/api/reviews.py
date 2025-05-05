from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src import database as db
import sqlalchemy

router = APIRouter(
    prefix="/sets",
    tags=["sets"]
)

@router.post("/{set_id}/reviews")
def add_review(set_id: int, user_id: int, rating: int, description: str):
    """
    Add a review for a specific Lego set.
    """
    if rating < 1 or rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO reviews (set_id, user_id, rating, description)
                VALUES (:set_id, :user_id, :rating, :description)
                """
            ),
            {"set_id": set_id, "user_id": user_id, "rating": rating, "description": description}
        )
    return {"message": f"Review added for set {set_id}"}
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from src import database as db
import sqlalchemy
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/sets",
    tags=["sets"]
)

class ReviewRequest(BaseModel):
    user_id: int
    rating: int = Field(..., ge=1, le=5, description="Rating must be between 1 and 5")
    description: str

@router.post("/{set_id}/reviews",status_code=status.HTTP_201_CREATED)
def add_review(set_id: int, review: ReviewRequest):
    """
    Add a review for a specific Lego set.
    """
    if review.rating < 1 or review.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO reviews (set_id, user_id, rating, description)
                VALUES (:set_id, :user_id, :rating, :description)
                """
            ),
            {"set_id": set_id, "user_id": review.user_id, "rating": review.rating, "description": review.description}
        )
    
    return {
        "message": f"Review successfully added.",
        "data": {
            "set_id": set_id,
            "user_id": review.user_id,
            "rating": review.rating,
            "description": review.description
        }
    }
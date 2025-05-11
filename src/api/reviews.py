from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from src import database as db
import sqlalchemy
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Literal

router = APIRouter(
    prefix="/sets",
    tags=["reviews"]
)

class ReviewRequest(BaseModel):
    user_id: int
    rating: int = Field(..., ge=1, le=5, description="Rating must be between 1 and 5")
    description: str

class ReviewResponse(BaseModel):
    review_id: int
    set_id: int
    user_id: int
    rating: int
    description: str
    created_at: datetime

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

@router.get("/{set_id}/reviews/average")
def get_average_rating(set_id: int):
    """
    Get the average rating for a set.
    """
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT AVG(rating) AS avg_rating
                FROM reviews
                WHERE set_id = :set_id
                """
            ),
            {"set_id": set_id}
        ).scalar()

    if result is None:
        raise HTTPException(status_code=404, detail="No reviews found for this set")

    return {"set_id": set_id, "average_rating": round(result, 2)}

@router.get("/{set_id}/reviews", response_model=List[ReviewResponse])
def get_all_reviews(
    set_id: int,
    sort_by: Literal["newest", "oldest", "score_asc", "score_desc"] = Query("newest", description="Sort order: newest, oldest, score_asc, score_desc")
):
    """
    Retrieve all reviews for a specific set, sorted by date or score.
    """
    sort_clause = {
        "newest": "created_at DESC",
        "oldest": "created_at ASC",
        "score_asc": "rating ASC",
        "score_desc": "rating DESC"
    }.get(sort_by, "created_at DESC")

    query = f"""
        SELECT review_id, set_id, user_id, rating, description, created_at
        FROM reviews
        WHERE set_id = :set_id
        ORDER BY {sort_clause}
    """

    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(query),
            {"set_id": set_id}
        ).fetchall()

    return [dict(row._mapping) for row in result]

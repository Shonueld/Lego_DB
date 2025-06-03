from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from src import database as db
import sqlalchemy
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Literal, Optional

router = APIRouter(
    prefix="/sets",
    tags=["reviews"]
)

class ReviewRequest(BaseModel):
    user_id: int
    rating: int = Field(..., ge=1, le=5, description="Rating must be between 1 and 5")
    description: str

class ReviewResponse(BaseModel):
    review_id: Optional[int] = None
    set_id: int
    user_id: int
    rating: int
    description: str
    created_at: Optional[datetime] = None

class ReviewMessageResponse(BaseModel):
    message: str
    data: ReviewResponse

class AverageRatingResponse(BaseModel):
    set_id: int
    average_rating: float

def validate_set_exists(connection, set_id: int):
    set_exists = connection.execute(
        sqlalchemy.text("SELECT 1 FROM sets WHERE id = :set_id"),
        {"set_id": set_id}
    ).scalar_one_or_none()

    if not set_exists:
        raise HTTPException(status_code=404, detail="Set ID does not exist.")


@router.post("/{set_id}/reviews", response_model=ReviewMessageResponse, status_code=status.HTTP_201_CREATED)
def add_review(set_id: int, review: ReviewRequest):
    """
    Add a review for a specific Lego set.
    """
    if review.rating < 1 or review.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    # Check if the has built set
    with db.engine.begin() as connection:
        validate_set_exists(connection, set_id)
        built_check = connection.execute(
            sqlalchemy.text(
                """
                SELECT 1 FROM lists
                WHERE user_id = :user_id AND set_id = :set_id AND status = 'built'
                """
            ),
            {"user_id": review.user_id, "set_id": set_id}
        ).scalar_one_or_none()

        if not built_check:
            raise HTTPException(status_code=400, detail="Set has not been built by the user.")
        
        existing_review = connection.execute(
            sqlalchemy.text(
                "SELECT review_id FROM reviews WHERE user_id = :user_id AND set_id = :set_id FOR UPDATE"
            ),
            {"user_id": review.user_id, "set_id": set_id}
        ).scalar_one_or_none()

        if existing_review:
            review_id = connection.execute(
                sqlalchemy.text(
                    """
                    UPDATE reviews
                    SET rating = :rating, description = :description, created_at = NOW()
                    WHERE user_id = :user_id AND set_id = :set_id
                    RETURNING review_id
                    """
                ),
                {
                    "rating": review.rating,
                    "description": review.description,
                    "user_id": review.user_id,
                    "set_id": set_id
                }
            ).scalar_one()
            message = "Review successfully updated."
        else:
            review_id = connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO reviews (set_id, user_id, rating, description)
                    VALUES (:set_id, :user_id, :rating, :description)
                    RETURNING review_id
                    """
                ),
                {
                    "set_id": set_id,
                    "user_id": review.user_id,
                    "rating": review.rating,
                    "description": review.description
                }
            ).scalar_one()
            message = "Review successfully added."

        created_at =  connection.execute(
            sqlalchemy.text("""
                SELECT created_at 
                FROM reviews
                WHERE review_id = :review_id
                """),
            {"review_id": review_id}
        ).scalar_one()
        

    print("\n\n\nReview ID:", type(review_id), "\n\n\n")
    return ReviewMessageResponse(
        message=message,
        data=ReviewResponse(
            review_id=review_id,
            set_id=set_id,
            user_id=review.user_id,
            rating=review.rating,
            description=review.description,
            created_at=created_at)
    )

@router.get("/{set_id}/reviews/average", response_model=AverageRatingResponse)
def get_average_rating(set_id: int):
    """
    Get the average rating for a set.
    """
    with db.engine.begin() as connection:
        validate_set_exists(connection, set_id)
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

    return AverageRatingResponse(set_id=set_id, average_rating=round(result, 2))

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
        validate_set_exists(connection, set_id)
        result = connection.execute(
            sqlalchemy.text(query),
            {"set_id": set_id}
        ).fetchall()

    return [
    ReviewResponse(
        review_id=row.review_id,
        set_id=row.set_id,
        user_id=row.user_id,
        rating=row.rating,
        description=row.description,
        created_at=row.created_at
    )
    for row in result
]


    #return [ReviewResponse(**dict(row._mapping)) for row in result]
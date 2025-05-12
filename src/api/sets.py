from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
import sqlalchemy
from src.api import auth
from enum import Enum
from typing import List, Optional
from src import database as db


router = APIRouter(
    prefix="/sets",
    tags=["sets"],
    dependencies=[Depends(auth.get_api_key)],
)


class Set(BaseModel):
    id: int
    set_number: str
    name: str
    year_released: int
    number_of_parts: int
    theme_name: str


@router.get("/{set_id}", status_code=status.HTTP_200_OK)
def get_set(set_id: int):
    """
    Retrieves details for a specific set by ID
    """
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT id, set_number, name, year_released, number_of_parts, theme_name
                FROM sets 
                WHERE id = :set_id
                """),
            {"set_id": set_id},
        ).fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Set not found")
        
        set_details = dict(result._mapping)

    return {"message": f"Displays details for set {set_id}",
            "set_details": set_details 
    }
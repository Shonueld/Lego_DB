from fastapi import APIRouter, Depends, Query
from typing import Optional, List
import sqlalchemy
from src import database as db
from src.api import auth

router = APIRouter(
    prefix="/sets",
    tags=["sets"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/", summary="Search LEGO sets with optional filters")
def search_sets(
    min_pieces: Optional[int] = Query(None, description="Minimum number of pieces"),
    max_pieces: Optional[int] = Query(None, description="Maximum number of pieces"),
    min_year: Optional[int] = Query(None, description="Minimum year of release"),
    max_year: Optional[int] = Query(None, description="Maximum year of release"),
    theme: Optional[str] = Query(None, description="Theme name to filter by"),
    name: Optional[str] = Query(None, description="Name of the set to search for"),
):
    """
    Search for LEGO sets using optional filters like piece count, year, and theme.
    """
    query = """
        SELECT id, set_number, name, year_released, number_of_parts, theme_name
        FROM sets
        WHERE 1=1
    """
    params = {}

    if min_pieces is not None:
        query += " AND number_of_parts >= :min_pieces"
        params["min_pieces"] = min_pieces

    if max_pieces is not None:
        query += " AND number_of_parts <= :max_pieces"
        params["max_pieces"] = max_pieces

    if min_year is not None:
        query += " AND year_released >= :min_year"
        params["min_year"] = min_year

    if max_year is not None:
        query += " AND year_released <= :max_year"
        params["max_year"] = max_year

    if theme is not None:
        query += " AND theme_name ILIKE :theme"
        params["theme"] = f"%{theme}%"

    if name is not None:
        query += " AND name ILIKE :name"
        params["name"] = f"%{name}%"

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query), params)
        sets = result.fetchall()

    return [dict(row._mapping) for row in sets]

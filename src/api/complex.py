from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta
import sqlalchemy

from src.api import auth
from src import database as db

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
    dependencies=[Depends(auth.get_api_key)],
)

class PopularSet(BaseModel):
    set_id: int
    name: str
    built_count: int

class StreakUser(BaseModel):
    user_id: int
    username: str
    streak_weeks: int

# Most popular sets built in a given month and year
@router.get("/popular-sets", response_model=List[PopularSet])
def get_most_popular_sets(month: int = Query(..., ge=1, le=12), year: int = Query(...)):
    with db.engine.begin() as conn:
        result = conn.execute(
            sqlalchemy.text("""
                SELECT s.id AS set_id, s.name, COUNT(*) AS built_count
                FROM lists l
                JOIN sets s ON s.id = l.set_id
                WHERE l.status = 'built'
                  AND DATE_PART('month', l.created_at) = :month
                  AND DATE_PART('year', l.created_at) = :year
                GROUP BY s.id, s.name
                ORDER BY built_count DESC
                LIMIT 10
            """),
            {"month": month, "year": year}
        )
        sets = result.fetchall()
    
    return [PopularSet(**dict(row._mapping)) for row in sets]
# Get users with the longest build streaks (at least one built status per week)
@router.get("/build-streaks", response_model=List[StreakUser])
def get_top_build_streaks():
    with db.engine.begin() as conn:
        result = conn.execute(
            sqlalchemy.text("""
                WITH user_dates AS (
                    SELECT user_id, DATE_TRUNC('week', created_at) AS week
                    FROM lists
                    WHERE status = 'built'
                    GROUP BY user_id, DATE_TRUNC('week', created_at)
                ),
                streaks AS (
                    SELECT user_id, week, 
                           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY week) AS rn
                    FROM user_dates
                ),
                grouped AS (
                    SELECT user_id, 
                           MIN(week) AS start_week,
                           MAX(week) AS end_week,
                           COUNT(*) AS streak_weeks
                    FROM (
                        SELECT user_id, week, week - (rn || ' weeks')::interval AS grp
                        FROM streaks
                    ) AS sub
                    GROUP BY user_id, grp
                )
                SELECT u.user_id, u.username, MAX(g.streak_weeks) AS streak_weeks
                FROM grouped g
                JOIN users u ON u.user_id = g.user_id
                GROUP BY u.user_id, u.username
                ORDER BY streak_weeks DESC
                LIMIT 10;
            """)
        )
        users = result.fetchall()
    
    return [StreakUser(**dict(row._mapping)) for row in users]
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
import sqlalchemy
from src.api import auth
from enum import Enum
from typing import List, Optional
from src import database as db
from faker import Faker
import random
from sqlalchemy import text


router = APIRouter(
    prefix="/million",
    tags=["million"],
    dependencies=[Depends(auth.get_api_key)],
)




class FollowActionResponse(BaseModel):
    message: str



def generate_username_set(count):
    fake = Faker()
    usernames = set()

    patterns = [
        lambda f, l, n: f"{f}.{l}{n}",
        lambda f, l, n: f"{f}_{l}{n}",
        lambda f, l, n: f"{f[0]}{l}{n}",
        lambda f, l, n: f"{f}{l}",
        lambda f, l, n: f"{l}{n}",
        lambda f, l, n: f"{f}-{l}{n}",
        lambda f, l, n: f"{f}.{l}.{random.randint(1,99)}",
        lambda f, l, n: f"{f}{n}{l[0]}",
        lambda f, l, n: f"{f.capitalize()}{l.capitalize()}{n}",
        lambda f, l, n: f"{l.lower()}{f.upper()}{n}"
    ]

    while len(usernames) < count:
        first = fake.first_name()
        last = fake.last_name()
        num = random.randint(1, 9999)

        # Randomly pick a pattern
        pattern = random.choice(patterns)
        username = pattern(first.lower(), last.lower(), num)

        if len(username) <= 50:
            usernames.add(username)

    return list(usernames)



@router.post("/users/{count}", response_model=FollowActionResponse, status_code=status.HTTP_200_OK)
def postnewUsers(count: int):
    if count < 1:
        raise HTTPException(status_code=400, detail="Count must be greater than 0")

    users = generate_username_set(count)
    num_added = 0

    with db.engine.begin() as connection:
    # Construct the bulk VALUES clause
        BATCH_SIZE = 50000
        for i in range(0, len(users), BATCH_SIZE):
            batch = users[i:i + BATCH_SIZE]
            values_clause = ", ".join([f"(:username{i})" for i in range(len(batch))])
            param_dict = {f"username{i}": name for i, name in enumerate(batch)}

            sql = text(f"""
                INSERT INTO users (username)
                VALUES {values_clause}
                ON CONFLICT (username) DO NOTHING
                RETURNING 1
            """)

            result = connection.execute(sql, param_dict).fetchall()
            num_added += len(result)  # Approximate count; won't include skipped duplicates
    return FollowActionResponse(message=f"{num_added} users were created")




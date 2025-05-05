from dataclasses import dataclass
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field, field_validator
from typing import List

import sqlalchemy
from src.api import auth
from src import database as db
import random

router = APIRouter(
    prefix="",
    tags=["issues"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/sets/{set_id}/issues", status_code=status.HTTP_204_NO_CONTENT)
def post_deliver_bottles(message: str, set_id: int, user_id: int):
   """
   Delivery of potions requested after plan. order_id is a unique value representing
   a single delivery; the call is idempotent based on the order_id.
   """
   print(f"(POST set issuse) message: {message} order_id: {set_id} user_id: {user_id}")


   with db.engine.begin() as connection:
       connection.execute(sqlalchemy.text(
           """
           INSERT INTO issues (set_id, user_id, description)
           VALUES (:set_id, :user_id, :message)
           """
       ),
           {"set_id": set_id,
           "user_id": user_id,
           "message": message}
       )


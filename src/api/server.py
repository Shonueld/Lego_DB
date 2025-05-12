from fastapi import FastAPI
from src.api import lists, users, reviews, issues, search, sets
from starlette.middleware.cors import CORSMiddleware

description = """
LEGO DB is a database of (almost) every lego set. Add friends, create your list, and build!.
"""
tags_metadata = [
    #{"name": "cart", "description": "Place potion orders."},
    #{"name": "catalog", "description": "View the available potions."},
    #{"name": "bottler", "description": "Bottle potions from the raw magical elixir."},
    #{
    #    "name": "barrels",
    #    "description": "Buy barrels of raw magical elixir for making potions.",
    #},
    #{"name": "admin", "description": "Where you reset the game state."},
    #{"name": "info", "description": "Get updates on time"},
    #{
    #    "name": "inventory",
    #    "description": "Get the current inventory of shop and buying capacity.",
    #},
]

app = FastAPI(
    title="Lego DB",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Sean Griffin, Yenny Ma, Thomas Hagos, Javier Medina"
    },
    openapi_tags=tags_metadata,
)

origins = ["https://potion-exchange.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

#
app.include_router(lists.router)
app.include_router(users.router)
app.include_router(reviews.router)
app.include_router(issues.router)
app.include_router(search.router)
app.include_router(sets.router)

@app.get("/")
async def root():
    return {"message": "Welcome to LegoDB"}

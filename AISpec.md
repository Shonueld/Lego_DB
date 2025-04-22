# API Specifications
__________________________

## 1. Get Lego Set Catalog – /sets/ (GET)
Retrieves a list of Lego sets with optional filters like theme, price range, piece count, or age range.

Query Parameters (optional):
- theme (e.g., "Star Wars")
- price_min, price_max
- pieces_max, pieces_min
- age_max, age_min
- sort_by (e.g., release_date, price, difficulty)

Response:

[
  {
    "set_id": "12345",
    "name": "Millennium Falcon",
    "theme": "Star Wars",
    "price": 159.99,
    "pieces": 1351,
    "age_range": "10-14",
    "release_date": "2007-06-15"
  },
  ...
]

## 2. View Set Details /sets/{set_id} (GET)
Returns full details for the specific set, including its rating and known issues

Response:

{
  "set_id": "12345",
  "name": "Millennium Falcon",
  "theme": "Star Wars",
  "price": 159.99,
  "pieces": 1351,
  "release_date": "2007-06-15",
  "avg_rating": 4.7,
  "known_issues": [
    "Missing piece long white brick 4x2",
    "Confusing instructions in step 12, do blah blah instead"
  ]
}

## 3. Mark Set Status /users/{user_id}/sets/{set_id} (PUT)
Updates the users status for a specific Lego set
(status could be wishlist, purchased, building, or built)

Request:

{
  "status": "wishlist" 
}

Response:

{ "success": true }

## 4. Submit a review /sets/{set_id}/reviews (POST)
Submit a review and a star rating 1-5 for a set

Request:

{
  "user_id": "abc123",
  "rating": 5,
  "review": "Very fun build wow"
}

Response:

{ "success": true }

## 5. Get reviews for a set /sets/{set_id}/reviews (GET)
Retrieve a list of reviews for a specific Lego set

Query Parameters (optional):
- sort_by: date, rating
- order: asc, desc

Response:

[
  {
    "user_name": "BrickGod90000",
    "rating": 4,
    "review": "Great set but too easy imo.",
    "timestamp": "2025-03-21T10:12:00Z"
  },
  ...
]

## 6. Add known issues /sets/{set_id}/issues (POST)
Add a known issue that a set has for other users to see

Request:

{
  "user_id": "abc123",
  "description": "Missing wheel in bag 3"
}

Response:

{ "success": true }

## 7. View Friends Build Activity /users/{user_id}/friends/activity (GET)
View a list of all your friends builds and statuses

Response:

[
  {
    "friend_name": "Lucas",
    "action": "built",
    "set_name": "Arcane League of Legends",
    "timestamp": "2025-04-11T14:32:00Z"
  },
  ...
]

## 8. Get List Progress /users/{user_id}/list/progress (GET)
Returns the user's list progress across all sets, showing how many sets they've wishlisted, purchased, are building, or have built.

Response:

{
  "total_listed": 12,
  "purchased": 5,
  "building": 3,
  "built": 2,
  "remaining": 2
}

## 9. Report Review /reviews/{review_id}/report (POST)
Add a report to someone elses review

Request:

{ "reason": "Offensive language" }

## 10. Add a Friend /users/{user_id}/friends (POST)
Adds a friend on the database

Request:

{ "friend_id": "user456" }

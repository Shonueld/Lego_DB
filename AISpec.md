# API Specifications
__________________________

## 1. Get Lego Set Catalog – /sets/ (GET)
- Retrieves a list of Lego sets with optional filters like theme, price range, piece count, or age range.

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

Reponse:

{
  "set_id": "12345",
  "name": "Millennium Falcon",
  "theme": "Star Wars",
  "price": 159.99,
  "pieces": 1351,
  "release_date": "2023-06-15",
  "avg_rating": 4.7,
  "known_issues": [
    "Missing piece #342",
    "Confusing instructions in step 12"
  ]
}

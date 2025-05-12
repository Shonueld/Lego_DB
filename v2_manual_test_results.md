## Example Flow 1 – Parent Searching for a Gift
Sarah is shopping for a Lego set for her 10-year-old son’s birthday. She wants something age-appropriate in difficulty, and knows that he likes Mario. 

1. (Assuming Sarah already has an account) Sarah starts by calling GET /sets with filters for age piece count under 500, with Mario theme, that came out after 2018 and piece count under 500 to find suitable gift options.
2. She finds a set and calls GET /sets/91234 to view more details about the set.
3. Satisfied with the difficulty and reviews, she calls PUT /users/sarah123/sets/91234 to mark it as "wishlist" so she doesn’t forget it.
4. Later, she purchases it and updates her status by calling PUT /users/sarah123/sets/91234 again, this time marking the status as "purchased."
 
# CURL #1:
curl -X 'GET' \
  'http://127.0.0.1:3000/sets/?min_pieces=1&max_pieces=500&min_year=1900&max_year=2020&theme=System&name=Medium%20Gift%20Set%20%28ABB%29' \
  -H 'accept: application/json' \
  -H 'access_token: brat'
# Response #1:
[
  {
    "id": 4,
    "set_number": "700.3-1",
    "name": "Medium Gift Set (ABB)",
    "year_released": 1949,
    "number_of_parts": 142,
    "theme_name": "System"
  }
]

 
# CURL #2:
curl -X 'GET' \
  'http://127.0.0.1:3000/sets/788' \
  -H 'accept: application/json' \
  -H 'access_token: brat'
# Response #2:
{
  "message": "Displays details for set 788",
  "set_details": {
    "id": 788,
    "set_number": "115-1",
    "name": "Building Set",
    "year_released": 1973,
    "number_of_parts": 190,
    "theme_name": "Basic Set"
  }
}

# CURL #3:
curl -X 'PUT' \
  'http://127.0.0.1:3000/lists/2/sets/788' \
  -H 'accept: application/json' \
  -H 'access_token: brat' \
  -H 'Content-Type: application/json' \
  -d '{
  "status": "wishlist"
}'
# Response #3:
{
  "message": "List entry for set 788 has been created with status 'wishlist'",
  "username": "bobby",
  "set_id": 788,
  "status": "wishlist"
}
 
# CURL #4:
curl -X 'PUT' \
  'http://127.0.0.1:3000/lists/sarah123/sets/1' \
  -H 'accept: application/json' \
  -H 'access_token: brat' \
  -H 'Content-Type: application/json' \
  -d '{
  "status": "purchased"
}'
# Response #4:
{
  "message": "List entry for set 1 has been updated with status 'purchased'",
  "username": "sarah123",
  "set_id": 1,
  "status": "purchased"
}

## Example Flow 3 – Tracking Wishlist Completion
Maya wants to see how far she’s gotten through her Lego wishlist and what’s left to buy and build.

1. Maya begins by calling GET /users/maya789/wishlist/progress to view her overall progress across all sets. The database tells her she’s wishlisted 10 sets, purchased 4, is building 2, has built 1, and has 3 remaining.
2. Curious about one of the remaining sets, she calls GET /sets/83726 to check the set’s details and decide whether to start it next.
3. Realizing that she already purchased this set last week, she updates her status by calling PUT /users/maya789/sets/83726 to mark it as "purchased."

 
# CURL #1:
curl -X 'GET' \
  'http://127.0.0.1:3000/lists/2/progress' \
  -H 'accept: application/json' \
  -H 'access_token: brat'
# Response #1:
{
  "message": "Displayed progress for user bobby",
  "progress": {
    "building": {
      "count": 0,
      "sets": []
    },
    "built": {
      "count": 0,
      "sets": []
    },
    "purchased": {
      "count": 0,
      "sets": []
    },
    "wishlist": {
      "count": 0,
      "sets": []
    }
  }
}

 
# CURL #2:
curl -X 'GET' \
  'http://127.0.0.1:3000/sets/50' \
  -H 'accept: application/json' \
  -H 'access_token: brat'
# Response #2:
{
  "message": "Displays details for set 50",
  "set_details": {
    "id": 50,
    "set_number": "1240-2",
    "name": "8 Road Signs",
    "year_released": 1955,
    "number_of_parts": 8,
    "theme_name": "Supplemental"
  }
}
 
# CURL #3:
curl -X 'PUT' \
  'http://127.0.0.1:3000/lists/maya789/sets/1' \
  -H 'accept: application/json' \
  -H 'access_token: brat' \
  -H 'Content-Type: application/json' \
  -d '{
        "status": "purchased"
      }'

# Response #3:
{
  "message": "List entry for set 1 has been created with status 'purchased'",
  "username": "maya789",
  "set_id": 1,
  "status": "purchased"
}

## Example Flow 4 – Getting Inspiration From Friends
Jim is new to legos and is unsure what sets to go for next. He decides to check out his friend Pam's profile for some inspiration.

1. He starts by calling GET /users/jim012/friends/activity to view what sets Pam has recently built, wishlisted, or reviewed.
2. He notices that Pam recently built and reviewed a "Hogwarts Castle" set, so he calls GET /sets/1819 to learn more about it.
3. Impressed by the theme and difficulty, Jim calls PUT /users/jim012/sets/1819 to mark it as "wishlist" so he can remember it for later.

 
# CURL #1: 
curl -X 'GET' \
  'http://127.0.0.1:3000/users/7/friends/8/activity' \
  -H 'accept: application/json' \
  -H 'access_token: brat'

# RESPONSE #1:
{
  "friend username": "Pam12345",
  "activity": [
    {
      "set id": 1819,
      "set name": "Gamma V Laser Craft",
      "status": "wishlist",
      "created at": "2025-05-12T02:22:32.913853+00:00"
    },
    {
      "set id": 900,
      "set name": "Lear Jet",
      "status": "built",
      "created at": "2025-05-12T02:21:40.712335+00:00"
    },
    {
      "set id": 100,
      "set name": "Sloping Ridge and Valley Bricks, Red",
      "status": "built",
      "created at": "2025-05-12T02:21:34.105437+00:00"
    },
    {
      "set id": 91,
      "set name": "LEGO Town Plan Wooden Board",
      "status": "wishlist",
      "created at": "2025-05-12T02:21:05.992547+00:00"
    }
  ]
}


# CURL #2
curl -X 'GET' \
  'http://127.0.0.1:3000/sets/1819' \
  -H 'accept: application/json' \
  -H 'access_token: brat'


# RESPONSE #2: 
{
  "message": "Displays details for set 1819",
  "set_details": {
    "id": 1819,
    "set_number": "6891-1",
    "name": "Gamma V Laser Craft",
    "year_released": 1985,
    "number_of_parts": 135,
    "theme_name": "Classic Space"
  }
}
 
# CURL #3:
curl -X 'PUT' \
  'http://127.0.0.1:3000/lists/jim012/sets/1' \
  -H 'accept: application/json' \
  -H 'access_token: brat' \
  -H 'Content-Type: application/json' \
  -d '{
  "status": "wishlist"
}'
# Response #3:
{
  "message": "List entry for set 1 has been created with status 'wishlist'",
  "username": "jim012",
  "set_id": 1,
  "status": "wishlist"
}
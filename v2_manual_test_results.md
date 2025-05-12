## Example Flow 1 – Parent Searching for a Gift
Sarah is shopping for a Lego set for her 10-year-old son’s birthday. She wants something age-appropriate in difficulty, and knows that he likes Mario. 

1. (Assuming Sarah already has an account) Sarah starts by calling GET /sets with filters for age piece count under 500, with Mario theme, that came out after 2018 and piece count under 500 to find suitable gift options.
2. She finds a set and calls GET /sets/91234 to view more details about the set.
3. Satisfied with the difficulty and reviews, she calls PUT /users/Sarah/sets/91234 to mark it as "wishlist" so she doesn’t forget it.
4. Later, she purchases it and updates her status by calling PUT /users/Sarah/sets/91234 again, this time marking the status as "purchased."
 
# CURL #1:
curl -X 'GET' \
  'http://127.0.0.1:3000/sets/?max_pieces=500&min_year=2018&theme=Mario' \
  -H 'accept: application/json' \
  -H 'access_token: brat'
# Response #1:
[
  {
    "id": 17673,
    "set_number": "5006216-1",
    "name": "Starter Kit Bundle with Gift",
    "year_released": 2020,
    "number_of_parts": 0,
    "theme_name": "Super Mario"
  },
  {
    "id": 17674,
    "set_number": "6288911-1",
    "name": "Character Pack Series 1 - Sealed Box",
    "year_released": 2020,
    "number_of_parts": 0,
    "theme_name": "Super Mario"
  },
  {
    "id": 17675,
    "set_number": "71361-0",
    "name": "Character Pack Series 1 - Random Bag",
    "year_released": 2020,
    "number_of_parts": 0,
    "theme_name": "Super Mario"
  },
  ... (Many more sets)
]

 
# CURL #2:
curl -X 'GET' \
  'http://127.0.0.1:3000/sets/19131' \
  -H 'accept: application/json' \
  -H 'access_token: brat'
# Response #2:
{
  "message": "Displays details for set 19131",
  "set_details": {
    "id": 19131,
    "set_number": "71384-1",
    "name": "Penguin Mario Power-Up Pack",
    "year_released": 2021,
    "number_of_parts": 18,
    "theme_name": "Super Mario"
  }
}

# CURL #3:
curl -X 'PUT' \
  'http://127.0.0.1:3000/lists/7/sets/19131' \
  -H 'accept: application/json' \
  -H 'access_token: brat' \
  -H 'Content-Type: application/json' \
  -d '{
  "status": "wishlist"
}'
# Response #3:
{
  "message": "List entry for set 19131 has been created with status 'wishlist'",
  "username": "Sarah",
  "set_id": 19131,
  "status": "wishlist"
}
 
# CURL #4:
curl -X 'PUT' \
  'http://127.0.0.1:3000/lists/7/sets/19131' \
  -H 'accept: application/json' \
  -H 'access_token: brat' \
  -H 'Content-Type: application/json' \
  -d '{
  "status": "purchased"
}'
# Response #4:
{
  "message": "List entry for set 19131 has been updated with status 'purchased'",
  "username": "Sarah",
  "set_id": 19131,
  "status": "purchased"
}

## Example Flow 3 – Tracking Wishlist Completion
Maya wants to see how far she’s gotten through her Lego list and what’s left to buy and build.

1. (Assuming Maya already has an account and items in her list) Maya begins by calling GET /users/Maya/list/progress to view her overall progress across all sets. The database tells her she’s wishlisted 4 sets, purchased 3, is building 1, and has built 1.
2. Curious about one of the remaining sets, she calls GET /sets/19145 to check the set’s details and decide whether to start it next.
3. Realizing that she already built this set last week, she updates her status by calling PUT /users/Maya/sets/19145 to mark it as "built."

 
# CURL #1:
curl -X 'GET' \
  'http://127.0.0.1:3000/lists/8/progress' \
  -H 'accept: application/json' \
  -H 'access_token: brat'
# Response #1:
{
  "message": "Displayed progress for user Maya",
  "progress": {
    "built": {
      "count": 1,
      "sets": [
        "Firefighter Bob with Equipment"
      ]
    },
    "wishlist": {
      "count": 4,
      "sets": [
        "Friends: Piżama Party",
        "Parachute Goomba",
        "Thwimp",
        "Torpedo Ted"
      ]
    },
    "purchased": {
      "count": 3,
      "sets": [
        "Builder with Epic Digger",
        "Garbage Truck and Recycling",
        "Performing Dog"
      ]
    },
    "building": {
      "count": 1,
      "sets": [
        "TIE Bomber"
      ]
    }
  }
}

 
# CURL #2:
curl -X 'GET' \
  'http://127.0.0.1:3000/sets/19145' \
  -H 'accept: application/json' \
  -H 'access_token: brat'
# Response #2:
{
  "message": "Displays details for set 19145",
  "set_details": {
    "id": 19145,
    "set_number": "952102-1",
    "name": "Builder with Epic Digger",
    "year_released": 2021,
    "number_of_parts": 21,
    "theme_name": "Construction"
  }
}
 
# CURL #3:
curl -X 'PUT' \
  'http://127.0.0.1:3000/lists/8/sets/19145' \
  -H 'accept: application/json' \
  -H 'access_token: brat' \
  -H 'Content-Type: application/json' \
  -d '{
  "status": "built"
}'

# Response #3:
{
  "message": "List entry for set 19145 has been updated with status 'built'",
  "username": "Maya",
  "set_id": 19145,
  "status": "built"
}
## Example Flow 4 – Getting Inspiration From Friends
Jim is new to legos and is unsure what sets to go for next. He decides to check out his friend Pam's profile for some inspiration.

1. (Assuming Jim already has an account with Pam, who is also active) He starts by calling GET /users/9/friends/10/activity to view what sets Pam has recently changed the status of, or reviewed.
2. He notices that Pam recently built and reviewed a Harry Potter set, so he calls GET /sets/19195 to learn more about it.
3. Impressed by the theme and difficulty, Jim calls PUT /users/Jim/sets/19195 to mark it as "wishlist" so he can remember it for later.

 
# CURL #1: 
curl -X 'GET' \
  'http://127.0.0.1:3000/users/9/friends/10/activity' \
  -H 'accept: application/json' \
  -H 'access_token: brat'

# RESPONSE #1:
{
  "friend username": "Pam",
  "activity": [
    {
      "set id": 19195,
      "set name": "Wizarding World Minifigure Accessory Set",
      "status": "built",
      "created at": "2025-05-12T20:44:57.950160+00:00"
    },
    {
      "set id": 19192,
      "set name": "Magical Ideas",
      "status": "purchased",
      "created at": "2025-05-12T20:44:51.495411+00:00"
    },
    {
      "set id": 19188,
      "set name": "Owen with Helicopter",
      "status": "purchased",
      "created at": "2025-05-12T20:44:46.679438+00:00"
    },
    {
      "set id": 19181,
      "set name": "Sinjin Prescott with Buggy",
      "status": "purchased",
      "created at": "2025-05-12T20:44:44.472903+00:00"
    },
    {
      "set id": 19180,
      "set name": "Harry Potter: Prépare-toi pour la magie!",
      "status": "built",
      "created at": "2025-05-12T20:44:38.443403+00:00"
    }
  ],
  "reviews": [
    {
      "set id": 19195,
      "set name": "Wizarding World Minifigure Accessory Set",
      "created at": "2025-05-12T20:48:05.730152+00:00",
      "rating": 1,
      "description": "Absolutely terrible, doesn't look like the photos"
    }
  ]
}


# CURL #2
curl -X 'GET' \
  'http://127.0.0.1:3000/sets/19195' \
  -H 'accept: application/json' \
  -H 'access_token: brat'


# RESPONSE #2: 
{
  "message": "Displays details for set 19195",
  "set_details": {
    "id": 19195,
    "set_number": "40500-1",
    "name": "Wizarding World Minifigure Accessory Set",
    "year_released": 2021,
    "number_of_parts": 33,
    "theme_name": "Harry Potter"
  }
}
 
# CURL #3:
curl -X 'PUT' \
  'http://127.0.0.1:3000/lists/9/sets/19195' \
  -H 'accept: application/json' \
  -H 'access_token: brat' \
  -H 'Content-Type: application/json' \
  -d '{
  "status": "wishlist"
}'
# Response #3:
{
  "message": "List entry for set 19195 has been created with status 'wishlist'",
  "username": "Jim",
  "set_id": 19195,
  "status": "wishlist"
}
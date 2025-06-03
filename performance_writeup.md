# Fake Data Modeling

Python scripts used to generate rows: Lego_DB/src/api/datafaking

- Must run fake_reviews and fake_issues after running fake_lists

Final rows of data in each table:

- Users: 50,000 rows
- Sets: 21,496 rows
- Reviews: 100,000 rows
- Lists: 500,000 rows
- Issues: 100,000 rows
- Followers: 200,000 rows
- Follow Log: 200,000 rows

Justification:
Our service would scale this way because the majority of our database would be storing users lists, as almost every user who cares enough to make an account to keep track of their lists is going to add a few sets. Each user we estimated follows around 4 others, which seems like a reasonable amount of friends who build legos the average lego enjoyer has, and 2 in every five sets added to a list are either reviewed or have an issue associated.

# Performance results of hitting endpoints

    - GET /popular-sets 26 ms
    - GET /build-streaks 183 ms
    - PUT /lists/{user_id}/sets/{set_id} 35ms
    - GET /lists/{user_id}/progress 44ms
    - POST /users 6ms
    - POST /users/{user_id}/follow 22ms
    - POST /users/{user_id}/unfollow 12ms
    - GET /users/{user_id}/following-list 24ms
    - GET /users/{user_id}/activity/{following_id} 33ms
    - POST /sets/{set_id}/reviews 26ms
    - GET /sets/{set_id}/reviews 23ms
    - GET /sets/{set_id}/reviews/average 20ms
    - POST /sets/{set_id}/issues 33ms
    - GET /sets/{set_id}/issues 44ms
    - GET /sets 23ms
    - GET /sets/{set_id} 11ms
    
# Performance tuning

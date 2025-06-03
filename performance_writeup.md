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
    - GET /build-streaks 183 ms (SLOWEST) -> 130ms
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

Explain before adding index:

Limit  (cost=31581.48..31581.51 rows=10 width=23)
  ->  Sort  (cost=31581.48..31612.71 rows=12490 width=23)
        Sort Key: (max((count(*)))) DESC
        ->  HashAggregate  (cost=31186.68..31311.58 rows=12490 width=23)
              Group Key: u.user_id
              ->  Hash Join  (cost=30654.29..31124.23 rows=12490 width=23)
                    Hash Cond: (streaks.user_id = u.user_id)
                    ->  HashAggregate  (cost=29192.29..29504.54 rows=12490 width=36)
"                          Group Key: streaks.user_id, (streaks.week - (((streaks.rn)::text || ' weeks'::text))::interval)"
                          ->  Subquery Scan on streaks  (cost=22947.32..28255.54 rows=124900 width=12)
                                ->  WindowAgg  (cost=22947.32..26382.04 rows=124900 width=20)
                                      ->  Group  (cost=22947.29..24196.29 rows=124900 width=12)
"                                            Group Key: lists.user_id, (date_trunc('week'::text, lists.created_at))"
                                            ->  Sort  (cost=22947.29..23259.54 rows=124900 width=12)
"                                                  Sort Key: lists.user_id, (date_trunc('week'::text, lists.created_at))"
                                                  ->  Seq Scan on lists  (cost=0.00..10239.25 rows=124900 width=12)
"                                                        Filter: ((status)::text = 'built'::text)"
                    ->  Hash  (cost=837.00..837.00 rows=50000 width=15)
                          ->  Seq Scan on users u  (cost=0.00..837.00 rows=50000 width=15)

The biggest problem we can see from this explain is the Seq Scan on lists. This means its scanning every single row in the list where status = 'built'. 

Index added:

CREATE INDEX idx_lists_status_user_created_week
ON lists (status, user_id, created_at);

Limit  (cost=16685.60..16685.63 rows=10 width=23)
  ->  Sort  (cost=16685.60..16716.83 rows=12490 width=23)
        Sort Key: (max((count(*)))) DESC
        ->  HashAggregate  (cost=16290.80..16415.70 rows=12490 width=23)
              Group Key: u.user_id
              ->  Hash Join  (cost=15758.41..16228.35 rows=12490 width=23)
                    Hash Cond: (streaks.user_id = u.user_id)
                    ->  HashAggregate  (cost=14296.41..14608.66 rows=12490 width=36)
"                          Group Key: streaks.user_id, (streaks.week - (((streaks.rn)::text || ' weeks'::text))::interval)"
                          ->  Subquery Scan on streaks  (cost=0.65..13359.66 rows=124900 width=12)
                                ->  WindowAgg  (cost=0.65..11486.16 rows=124900 width=20)
                                      ->  Group  (cost=0.56..9300.41 rows=124900 width=12)
"                                            Group Key: lists.user_id, (date_trunc('week'::text, lists.created_at))"
                                            ->  Incremental Sort  (cost=0.56..8363.66 rows=124900 width=12)
"                                                  Sort Key: lists.user_id, (date_trunc('week'::text, lists.created_at))"
                                                  Presorted Key: lists.user_id
                                                  ->  Index Only Scan using idx_lists_status_user_created_week on lists  (cost=0.42..4982.42 rows=124900 width=12)
"                                                        Index Cond: (status = 'built'::text)"
                    ->  Hash  (cost=837.00..837.00 rows=50000 width=15)
                          ->  Seq Scan on users u  (cost=0.00..837.00 rows=50000 width=15)
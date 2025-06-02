Code Review Comments:

1. /lists/{user_id}/sets/{set_id} gave me : Internal Server Error, maybe there are too many options so it is too slow?
- Hard to say exactly why this happened without the details from their terminal, its liekly that the set didnt exist and thats why it 500'd however. Added a check to make sure a set_id exists before adding it to your list.
2. /sets/{set_id}/reviews I put set id 1 and user id 1, rating 2 description bad and it gave me : Internal Server Error
- I was able to do it on my end, but a different issue is that users who didnt build the set could still review it, so we added that constraint
3. /sets/{set_id}/issues i had input set id 1, user id 1, Internal Server Error
- Issues now makes sure that the user has the list in their set, the set exists, and that the user exists
4. /sets/ - bad input such as negative number isn't caught and just breaks also. There should be some sort of checks to make sure these inputs are valid numbers, if it is negative just make it equal to 0, make an error saying that
- Using negative numbers doesn't break the query, it does just act as a zero which I think is as expected, would need a more specific example of what caused the error
5. /sets/{set_id}/reviews the post and get are the same here, not sure if this would cause confusion, maybe just change to add Review and search review, same with friends, and issues?
- That's standard RESTful format, the same routes but one being POST and the other being GET is completely normal
6. for reviews of a set there should be some limitation to prevent spamming or some negative words that could be inappropriate.
- Users are now limited to one review per set, and their review will get updated instead if they try to post a new review for a set they have already reviewed. 
7. implement logging when creating users and adding friends so you have an easier way to see history
- Added a new follow_log to keep track
8. add more detail to friends, there is no way to accept or decline it is just a one way decision
- We ended up pivoting from friends to followers, as we felt one way behaviour made more sense
9. /sets/ if max and min are switched this wouldn't make sense instead we can test for this special case or if max and min are equal
- I feel like that behaves as you would expect, if min is higher than max they no sets are returned
10. updates status doesn't catch if the updated status is same as previous and will say updated, this is not true because nothing changed
- Lists now checks the current status, and says "List entry for set X already has status 'status_name'
11. overall everything took forever to run on my end, not sure if this is because of your code or on my end but it isn't happening in my other projects so definitely something to look into, maybe you can make things more efficient on your end.
- Probably a result of using a large database of 25000 sets, but no one else has had this issue, and the render deployment hasnt either
12. overall more precise error messages would be helpful
- Addressed from the previous changes that no longer just return 500s


1. Under @router.get("/{user_id}/friends/{friend_id}/activity", status_code=status.HTTP_200_OK) and @router.get("/{user_id}/friends", status_code=status.HTTP_200_OK) both functions are called get_friends
- Function name was changed on both endpoints  

2. When creating users or adding friends, there can be logging implemented to allow for easier backend debugging.
- Table added to log and see which user is following who.

3. On @router.post("/{user_id}/friends", status_code=status.HTTP_201_CREATED), where it returns {"message": "Invalid ids or attempting to enter duplicates"}, it could be more clear as to whether it is because of invalid ids or attempting to enter duplicates.
- Added two error messages: one to indicate if a user is already following another user, and another if the user being followed does not exist.

4. user_id is fetched multiple times, a abstract helper function can help reduce repetition
5. In sets.py and other files where a dictionary is being returned, response models can be used for clarity.
6. Friends for now stores a one directional friendship, a bidirectional design may make more sense. If you wanted to keep it one directional, perhaps a follower and following may make more sense.
7. Validation to check if foreign keys exist should be implemented before attempting inserts, like seeing if set_id in /sets/{set_id}/reviews actually exists.
8. For sets, id is referred to as sets.id, while for users, id is called user_id. Standardizing this for primary keys across the tables can make it less error prone.
9. Some files import Enum and Optional without ever using them.
10. In reviews.py, the sort_clause is hardcoded into the get_all_reviews function. sort_clause can be its own function so that it can also be called in users.py when getting friend’s reviews.
11. Something should be implemented to prevent a user from putting multiple reviews on a set.
12. When dict(row._mapping) is used on return statements; there should be a response model so that it is consistent throughout the other files that also return a dictionary.


1. Under the endpoint users/{user_id}/friends/{friend_id}/activity
Error in logic where if the friend has no activity, it returns "Not Friends" even if they are friends
This is at line 156 of users.py
- Edited the endpoint to add an error that returns a separate error if the requested user has no activity
- Endpoint no longer returns "Not Following" when there is no activity available
2. Under the endpoint lists/{user_id}/progress there is a redudant Order By Query
The comment on line 103 of lists.py specifies its meant to group by the status, which is great if we are meant to be viewing this query.
However, it immediately sorts the results queried into a dictionary meaning the order by isn't neccessary.
-   Removed the ORDER BY query to reduce redundancy
3. Friends are not mutual when adding. User 1 could be friends with User 2, yet User 2 is not friends with User 1.
-   Replaced friends with followers, which intentionally use a one-way relationship
Maybe implement a method of confirming friendship, or not counting as friends until it is mutual.
4. Under add_friends in users.py, if inputting the same user id (Example: User 1 adding User 1 as a friend) it returns internal server error
- Added error checking for when a user tries to follow itself
5. line 108 in users.py returns "User Not Found" but should properly use a HTTPException to exit the code
- Added a HTTPException in get_following_users function with status.HTTP_404_NOT_FOUND for when a user does not exist
6. get_friends function has 2 separate Queries to get Username and Friends, but could be combined into 1 Query
- While it is possible to combine these two queries, we have decided to leave them separate to enable error checking throughout the function. If we combined them and the query returned no result, we would not be able to tell if the result was empty because the user does not exist, or if it was empty because the user was not following anyone.
7. line 76 of users.py is using result.rowcount to determine if its an invalid id or duplicate which is ambiguous when testing. This could instead be separated to allow for a more precise error message.
- Added error checking to get_following function make it less ambiguous as to the reason for error
8. This is a continuation of issue #7 as it returns a dictionary response when it should properly return an HTTPException to exit the code.
- Added furthing error checking in get_user_activity_feed function to remove all dictionary responses
9. lines 50-60 on lists.py are updating the status. However, if the updated status is the same as the previous status, it still returns the message "updated" even though no change occured.
-   update_list_status function now checks to see if the new status is the same as the previous one
-   It alters the message to say "List entry for set {set_id} already has status '{body.status}'"
10. Continuation of Issue 1
Not entirely sure why this is happening, but even if there is activity it just returns "Not Friends"
- Fixed through the fix for issue 1
11. Overall using dicts to return data instead of using Pydantic models. This is fine but Pydantic models allows for better control and modifying of the code in the future.
-   Replaced all dictionaries in ending return statements with Pydantic models for all API endpoints
12. When trying to update the status of a set that doesn't exist, there isn't a catch for that, meaning it returns an Internal Server Error.
-   There already exists error checking for when a set doesn't exist in the update_list_status function.

API Design Comments:

1. /users/{user_id}/friends gave me :
{
"message": "Invalid ids or attempting to enter duplicates"
}
- Endpoint No longer Used**
2. /sets/ wont give me anything if I don't use the filters but in description says optional
- Works as intended for me? more testing needed**
3. add feature to block friend request, maybe there is someone who you don't want to be associated with
- Added /users/{user_id}/block and unblock**
4. add feature to report user for misconduct such as bad comments being posted
- in progres, just need to update schema with new tables and add unblock logic**
5. something that lists suggested friends because otherwise how would you know what their id is
- Great suggestion, can display users that 1. have alot of followers 2. have alot of sets in list 3. suggest friends based on user list similarity**
6. add some sort of leaderboard feature so that there is a community aspect
- Can add different criterias based on amount reviewed, most completed, followers etc**
7. I think it would be cool to add not only other users as friends but groups so people with similar interests, locations, or projects can talk and be in a sub group
- Great idea, however communication between friends is not supported, this can be accounted for when creating suggested friends to help create link friends of friends together and establish groups in a sense**

8. I feel like adding a time stamp to when the friendship was created could be nice for tracking and also a fun leaderboard later for longest friendships
- feels a bit unecessary to make a leaderboard however adding a timestamp seems like a good idea
9. Also a timestamp on when the issues were published would be good because if it gets resolved a time stamp would help a user figure out when it was reported and if that is an old or new issue
- Great suggestion
10. for the review I think it would be good to add the user id of the person who submitted it, this information wouldn't be shared but it would be stored in case something bad is posted or someone is spamming then you know who is the problem
- Great suggestion
11. maybe some sort of feature where friends could collaborate on a lego project, so some way to add multiple people to project
- It would be smoother to have them seperate, details about the build could always go in the review
12. not sure if it would be helpful to make the id labels more specific so if you are doing quarries and joining tables it is easier for readability.
- not a bad suggestion, could always just lable the table then do table_name.id

1. For user_id and friend_id, the use of unique when creating the alembic table can be used to prevent duplicates.
- could add that, we already check for duplicates though
2. On lists.py, the lists.status column accepts arbitrary strings. ENUM can be used so that only {"wishlist", "purchased", "building", "built"} are accepted.
- Switched to using ENUM
3. For reviews and list entries, an updated_at timestamp can make tracking entries easier.
- already mentioned, good idea
4. post_issue() returns both user_id and username, which can be redundant.
- I think its good to return both, knowing user_id is useful if you want to continuously test  endpoints, same goes with username
5. The review structure in friend activity is inconsistent with the review structure in reviews.
- not sure what this means
6. The ability to delete users, friends, sets from lists, and reviews should be implemented.
- great idea
7. A primary key id for the friends table can help with management and tracking.
- primary key would be unecessary, it uses a composite key which can do the same thing
8. For status and username, it should not be allowed to be NULL.
- status was changed to only accept certain options, username minimum size is 1 character
9. Username should have a character limit just so that the data is more consistent.
- added username cap of 50 characters
10. Users should only be able to leave one review per set, so a unique constraint should be implemented.
- User could leave only 1 review, if it tries to resubmit a review it will override the old one
11. For lists, users should also only be able to have one entry per set so a unique constraint should also be added.
- previously mentioned
12. CHECK constraints for reviews.rating can be implemented in the database columns even though it may be added in reviews.py
- Already test for duplicate entries
1. API Endpoint /sets is very slow and returns too many results.
Perhaps limit the return results.
- Limited results to 50 by default and added an option to choose how many to return, now paginates results
2. Under API Endpoint /lists/{user_id}/sets/{set_id}, make it a dropdown to change the status instead of a json input that can be mistyped
- I dont think this is an issue, no user would actually be interacting with our endpoints like this
3. for API Endpoint sets/{set_id} maybe rename to have a bit more detail such as sets/info/{set_id}
- I think its fine as it is, you get the set with the given ID, and you get all of its details
4. API Endpoint /sets/{set_id}/issues does not have a limit
Perhaps limit the return results
- Same thing as resolving issue 1, added pagination
5. Create constraints on valid set id. (User is able to input negative ids which don't exist)
- If a user calls GET /sets on a negative ID it says set not found as you would expect
6. Issues API Endpoints is labeled as /sets
- Because they are issues with the set
7. Reviews API Endpoints is labeled as /sets
- Because they are reviews on the sets
8. Reviews are able to have no description (not sure if that is intended)
- Intended
9. Issues are able to have no description (pretty sure thats not intended)
- Issues now requires users to input a description that is not empty
10. I feel like Reviews should have a similar return message format as Issues.
Currently it doesn't return username, created_at, or the id of the review itself which creating an Issue has in it's response message
- Reviews currently returns a message (added/updated) set_id, user_id, rating, and description which I feel is sufficient
- added review_id and created_at in the return type
11. API Endpoint for /users/{user_id}/friends are duplicated. One is for POST and one is for GET.
Rename them to distinguish them apart since this could potentially create conflicts.
- This is standard RESTful and shouldn't be changed
12. API Endpoint for /sets/{set_id}/reviews are duplicated. One is for POST and one is for GET.
Rename them to distinguish them apart since this could potentially create conflicts.
- This is standard RESTful and shouldn't be changed
13. API Endpoint for /sets/{set_id}/issues are duplicated. One is for POST and one is for GET.
Rename them to distinguish them apart since this could potentially create conflicts.
- This is standard RESTful and shouldn't be changed

Lucas Pierce Comments:
1. What is the point of /users/{user_id}/friends/{friend_id}/activity? Why not just have a get activity endpoint for users?

2. /sets/ with no query parameters doesn’t return. At the very least put a limit, but even better paginate the results.
- Paginated the results so it works without paramaters

3. /lists/{user_id}/sets/{set_id} gives internal server error when given some inputs.


Some funky code (like running a count(*) where username to look for a name already existing). The peer reviews did a good job of catching major issues. You got some great peer review feedback (and some not good advice ). Please address all of it or call out why you don’t think it should be addressed individually. Overall, one of the better projects, you did a great job. If you address feedback by June 2nd AND send me a message, I will give you points back

 
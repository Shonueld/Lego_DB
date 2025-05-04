## Example Flow 1 – Parent Searching for a Gift
Sarah is shopping for a Lego set for her 10-year-old son’s birthday. She wants something age-appropriate, under $60, and not too complex.

1. Sarah starts by calling GET /sets with filters for age under 13, price under $60, and piece count under 500 to find suitable gift options.
2. She finds a "Lego City Fire Truck" and calls GET /sets/91234 to view more details about the set.
3. Satisfied with the difficulty and reviews, she calls PUT /users/sarah123/sets/91234 to mark it as "wishlist" so she doesn’t forget it.
4. Later, she purchases it and updates her status by calling PUT /users/sarah123/sets/91234 again, this time marking the status as "purchased."

## Example Flow 2 – Builder Reviews a Completed Set
Alex just finished building the massive Millennium Falcon set and wants to document his experience and help other builders.

1. He starts by calling PUT /users/alex456/sets/12345 to mark the set as "built."
2. Then, he calls POST /sets/12345/reviews to leave a 5-star review with a comment about how detailed and enjoyable the build was.
3. Noticing that a brick was missing from one of the bags, he also calls POST /sets/12345/issues to report a known issue about the missing piece in bag 3.

## Example Flow 3 – Tracking Wishlist Completion
Maya wants to see how far she’s gotten through her Lego wishlist and what’s left to buy and build.

1. Maya begins by calling GET /users/maya789/wishlist/progress to view her overall progress across all sets. The database tells her she’s wishlisted 10 sets, purchased 4, is building 2, has built 1, and has 3 remaining.
2. Curious about one of the remaining sets, she calls GET /sets/83726 to check the set’s details and decide whether to start it next.
3. Realizing that she already purchased this set last week, she updates her status by calling PUT /users/maya789/sets/83726 to mark it as "purchased."

## Example Flow 4 – Getting Inspiration From Friends
Jim is new to legos and is unsure what sets to go for next. He decides to check out his friend Pam's profile for some inspiration.

1. He starts by calling GET /users/jim012/friends/activity to view what sets Pam has recently built, wishlisted, or reviewed.
2. He notices that Pam recently built and reviewed a "Hogwarts Castle" set, so he calls GET /sets/1819 to learn more about it.
3. Impressed by the theme and difficulty, Jim calls PUT /users/jim012/sets/1819 to mark it as "wishlist" so he can remember it for later.

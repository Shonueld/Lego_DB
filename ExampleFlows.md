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

1. She begins by calling GET /users/maya789/list/progress to view her overall progress across all sets.
2. The database tells her she’s wishlisted 10 sets, purchased 4, is building 2, has built 1, and has 3 remaining.
3. Realizing that she recently bought one of the remaining sets, she updates her status by calling PUT /users/maya789/sets/83726 to mark it as "purchased."

## Example Flow 4 – Tracking Friends Progress
Jim is new to legos and is unsure what sets to go for next. He decides to check out his friend Pam's profile for some inspiration.

1. he begins by calling GET /users/Jim012/friends/pam012 to view her overall progress across all sets.
2. Jim receives Pam's whishlist, in-progress, and built lego sets alongside her reviews and ratings if available.
3. After looking through the options Jim decides to add one of these sets to his wishlist so he calls POST /users/jim012/list/set/1819

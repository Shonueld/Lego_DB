User Stories -

1. As someone who likes to talk about Legos with my friends, I want to be able to add friends, and view what sets they have completed/wishlisted.
2. As a parent who is unfamiliar with Lego and buying a gift for their child, I want there to be filters like “for children’s birthday”, that automatically applies other filters like age range under 13, and piece count below 500 so I can quickly look through what to buy.
3. As someone who doesn’t have a lot of time to build Legos, I want to be able to sort the sets that can be built in under an hour.
4. As a Lego enthusiast, I want to mark which sets I want to buy, have purchased, am building, or have built, so I can easily track my collection and building progress across all my sets.
5. As a Lego builder who has built sets with missing pieces or incorrect instructions before, I want there to be some “known issues” section I can write these problems to, and inform others of how to resolve it.
6. As a collector browsing the database, I want to filter sets by attributes like piece count, release year, theme, or price, and search by keywords or set names, so I can quickly mark sets I finished or discover new ones that match my interests.
7. As a parent looking for a gift, I want to see age recommendations and difficulty levels for each set, so that I can choose the right set for my child. 
8. As someone who is sticking to a budget, I want to view each Lego set by price range (ae. $0-50,50-100,100+) , so that I can find sets that fit within the budget that I am willing to spend. 
9. As a fan of specific Lego themes, I want to be able to filter themes like “Star Wars” or “Marvel”, and mark my wish lists current completion so that I can keep track of new releases for each theme. 
10. As a Lego reseller, I want to be able to view the current price and MSRP of different Lego sets, so that I can find the sets with the highest potential for profit.
11. As a child who is interested in Legos, I want to be able to find sets that are both cheap and released recently, so that they are easy to find in a retail store and I have enough money to buy them.
12. As someone who travels often, I want to be able to determine which Lego sets have fewer bricks and shorter build times, so that I can find sets that are portable and easy to travel with.

User Exceptions -

1. Exception: A users’ submission is too long causing an overflow. The expected behavior is to place a size limit on each input and notify user when going over the limit
2. Exception: User attempts a search with no parameters. The expected behavior would be to continue to display the sets that were before the search, or prompt the user that they need to search with some parameter or keyword
3. Exception: A user inputs their completed set time < 0, etc. The expected behavior is to prevent submission and warn the user of their error.
4. Exception:  A user enters a combination of filters for lego sets that returns no results. The expected behaviour would be for it to either display text saying “No results”, or a Did you mean …? suggestion.
5. Exception: A user attempts to submit a second review for a Lego set they've already reviewed. The system should either prevent the second review and inform the user they’ve already submitted one, or allow them to update their existing review instead.
6. Exception: A user tries to leave a review or star rating for a set they haven’t marked as "built." The system should block the review and prompt the user to mark the set as "built" before submitting a rating, to ensure ratings come from actual builders.
7. Exception: A user wants to search for a series with a special character (a.e. Pokémon), but the filter does not count “e” and “é” as the same letter. The system should treat these similar characters as identical, and still display “Pokémon” related entries if you search “Pokemon”.
8. Exception: A user loses internet connection while submitting a review or updating sets they have completed. The system should save the user’s input locally and try to resubmit automatically once their internet comes back, or tell the user that they lost connection, instead of hitting submit and being under the impression their review was sent. 
9. Exception: A user uploads inappropriate or spam content in a review. The system should flag the content and prevent the submission or send it for review, with a message explaining the content.
10. Exception: When leaving a review, a user leaves one of the required fields blank. The expected behaviour would be to not submit the review and to prompt the user for fields they must include.
11. Exception: A user attempts to add a set to their wishlist but the set has been discontinued. The system should still allow users to add sets to their wishlist, but alert the user and display that status on the set’s page.
12. Exception: A user tries to access a set’s details, but the details are missing or incomplete. The system should display that the information is unavailable or missing and suggest users to check back at a later time.

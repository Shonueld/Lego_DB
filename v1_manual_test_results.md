# Example Flow 2 – Builder Reviews a Completed Set
 
Alex just finished building the massive Millennium Falcon set and wants to document his experience and help other builders.

He starts by calling PUT /users/alex456/sets/12345 to mark the set as "built."

Then, he calls POST /sets/12345/reviews to leave a 5-star review with a comment about how detailed and enjoyable the build was.
Noticing that a brick was missing from one of the bags, he also calls POST /sets/12345/issues to report a known issue about the missing piece in bag 3.


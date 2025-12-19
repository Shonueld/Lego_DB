# Lego_DB
A database application designed to catalog, track, and review Lego sets. This project was developed for CSC 365 (Introduction to Databases) at Cal Poly SLO.

Lego DB is a centralized database platform for Lego enthusiasts to manage their collections. It has every existing Lego set's release date, price, pieces, etc. Users on the platform are able to mark which sets they want to buy, have purchased, are building, have built, and leave reviews on sets they have built with a star rating. This rating is then calculated as an average between all users.

# Tech Stack
- Backend: Python, FastAPI, Supabase
- Database: MySQL
- Containerization: Docker
- API Architecture: RESTful CRUD operations

# Key Features
- Users can track sets across five distinct states: Wishlist, Purchased, Building, Completed, and Reviewed.
- Implemented logic to calculate average star ratings.
- Integrated search and filtering features modeled after modern review platforms.
- Designed to handle thousands of unique Lego sets while maintaining data integrity between user profiles and the global catalog.

# Developers
- Sean Griffin (sgriff30@calpoly.edu)
- Thomas Hagos (thagos@calpoly.edu)
- Javier Medina Bueno (medinabu@calpoly.edu)
- Yenny Ma (yyma@calpoly.edu)


# Local Development & Testing
To run your server locally:

**1. Install Dependencies**

* Run ```uv sync``` in terminal

**2. Set Up Docker**

* Run the following command in terminal:
    ~~~
    docker run --name LegoDB -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydb -p 5432:5432 -d postgres:latest
    ~~~
* In the future, you can start the container by just running: ```docker start LegoDB```

**3. Upgrade Database to Latest Schema**

* Upgrade the database to your latest schema
    ~~~
    uv run alembic upgrade head
    ~~~

**4. Create New Connection**

* Install TablePlus (Can use DBeaver as well but haven't used myself)
* Create a new connection in TablePlus with PostgreSQL
    * Set name to "LegoDB"
    * Set "User" to myuser
    * Set "Password" to mypassword
    * Set "Databse" to mydatabase

**5. Update .env**

* Modify your modifythis.env file to the following:
~~~
Rename to: default.env
API_KEY=brat
POSTGRES_URI=postgresql+psycopg://myuser:mypassword@localhost/mydatabase
~~~
##Casting Agency Specifications
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

##Setup
Python 3.7
Follow instructions to install the latest version of python for your platform in the python docs

Dependencies
Use pip to install the dependencies
pip install -r requirements.txt

Heroku: https://udacity-casting-app.herokuapp.com/

##Authentication Setup
You can authenticate using the JWT tokens in test_app.py and SampleJWT.txt. These are valid until 3/25/2020.

New tokens can be pulled using the postman collection called udacity-getjwt-capstone


##Models:
Movies with attributes title and release date
Actors with attributes name, age and gender

##Endpoints:
GET /actors and /movies
DELETE /actors/ and /movies/
POST /actors and /movies and
PATCH /actors/ and /movies/

Get /actors
Returns all actors

{
  "success": true,
  "actors": [
    {
      "id": 1,
      "name": "test_actor",
      "age": 35,
      "gender": "female",
      "movie_id": 1
    },
    {
      "id": 1,
      "name": "updated_actor",
      "age": 30,
      "gender": "female",
      "movie_id": 1
    }
  ],
}

Get /movies
Returns all actors

{
  "success": true,
  "movies": [
    {
      "id": 1,
      "title": "test_movie",
      "release_date": "Thu, 05 Jan 2020 00:00:00 GMT",      
    },
    {
      "id": 2,
      "title": "updated_movie",
      "release_date": "Thu, 05 Jan 2020 00:00:00 GMT",
    }
  ],
}

Post /actors
Adds an actor

{
  "success": true,
  "actor":
    {
      "id": 1,
      "name": "test_actor",
      "age": 35,
      "gender": "female",
      "movie_id": 1
    }
}

Post /movies
Adds a movie

{
  "success": true,
  "movies":
    {
      "id": 1,
      "title": "test_movie",
      "release_date": "Thu, 05 Jan 2020 00:00:00 GMT",      
    }
}

Patch /actors/actor_id
Updates an actor of specified id

{
  "success": true,
  "actor":
    {
      "id": 2,
      "name": "updated_actor",
      "age": 30,
      "gender": "female",
      "movie_id": 1
    }
}

Patch /movies/movie_id
Updates a movie of specified id

{
  "success": true,
  "movies":
    {
      "id": 2,
      "title": "updated_movie",
      "release_date": "Thu, 05 Jan 2020 00:00:00 GMT",      
    }
}

Delete /actors/actor_id
Removes an actor of specific id

{
  "success": true,
  "actor":
    {
      "id": 2,
      "name": "updated_actor",
      "age": 30,
      "gender": "female",
      "movie_id": 1
    }
}

Delete /movies/movie_id
Removes a movie of specific id

{
  "success": true,
  "movies":
    {
      "id": 2,
      "title": "updated_movie",
      "release_date": "Thu, 05 Jan 2020 00:00:00 GMT",      
    }
}

##Roles:
Casting Assistant
Can view actors and movies
- get:actors
- get:movies

Casting Director
All permissions a Casting Assistant has and
Add or delete an actor from the database
Modify actors or movies
- delete:actors
- get:actors
- get:movies
- patch:actors
- patch:movies
- post:actors

Executive Producer
All permissions a Casting Director has and
Add or delete a movie from the database
- delete:actors
- delete:movies
- get:actors
- get:movies
- patch:actors
- patch:movies
- post:actors
- post:movies


##Tests:
One success test for each endpoint
One fail test for each endpoint
One test for each role for each endpoint 

Run the test using python test_app.py
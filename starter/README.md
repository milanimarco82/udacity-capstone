# Capstone-Project - Casting Agency

This is the final project of the Udacity Full Stack Developer NanoDegree Program. The goal of this project is to deploy a Flask application with Render/PostgreSQL and enable Role Based Authentication and Roles-Based Access Control (RBAC) with Auth0.

## Getting Started

### Installing Dependencies

1. **Python 3.7**

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment**

I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies**

Once you have your virtual environment setup and running, install dependencies by running:

```bash
$ pip install -r requirements.txt
```

This will install all the required packages we selected within the `requirements.txt` file.

4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Running the server

To run the server, execute:

```bash
$ source setup.sh
$ export FLASK_APP=app.py
$ export FLASK_ENV=development
$ flask run -- reload
```

Running `setup.sh` sets some environment variables used by the app.

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to use this file to find run application.

The `--reload` flag will detect file changes and restart the server automatically.

## Models:

- **Movies** model defined with the following attributes:
  - title 
  - release date


- **Actors** model defined with the following attributes:
  - name
  - age
  - gender

Models can be found in `models.py` file.

## Endpoints:

`GET '/movies'`
- Request Arguments: None
- Returns: A list of movies `movies`, all the movies from Movie table.
- 
```json
{
    "movies": [
        {
            "id": 9,
            "release_date": "Wed, 31 Dec 2025 23:00:00 GMT",
            "title": "Test Movie"
        },
        {
            "id": 11,
            "release_date": "Wed, 31 Dec 2025 23:00:00 GMT",
            "title": "Test Movie"
        }
    ],
    "success": true
}
```

---

`GET '/actors'`
- Request Arguments: None
- Returns: A list of actors `actors`, all the actors from Actor table.
- 
```json
{
    "actors": [
        {
            "age": 40,
            "gender": "M",
            "id": 1,
            "name": "John Doe"
        }
    ],
    "success": true
}
```

---

`DELETE '/actors/${id}'`

- Deletes a specified Actor using the id of the Actor
- Request Arguments: `id` - integer
- Returns: The id of the deleted Actor, in case of success
```json
{
  "deleted_id": 24
}
```
---

---

`DELETE '/movies/${id}'`

- Deletes a specified Movie using the id of the Movie
- Request Arguments: `id` - integer
- Returns: The id of the deleted Movie, in case of success
```json
{
  "deleted_id": 18
}
```
---

`POST '/actors'`

- Sends a post request in order to add a new Actor
- Request Body:

```json
{
  "name": "New actor",
  "age": 42,
  "gender": "M"
}
```
- Returns: A list containing the newly created Actor, in case of success
```json
{
    "actors": [
        {
            "age": 42,
            "gender": "M",
            "id": 31,
            "name": "New actor"
        }
    ],
    "success": true
}
```
---

`POST '/movies'`

- Sends a post request in order to add a new Movie
- Request Body:

```json
{
    "title": "New movie",
    "release_date": "01-Jan-2025"
}
```
- Returns: A list containing the newly created Movie, in case of success
```json
{
    "movies": [
        {
            "id": 17,
            "release_date": "Tue, 31 Dec 2024 23:00:00 GMT",
            "title": "New movie"
        }
    ],
    "success": true
}
```
---

`PATCH '/movies/${id}'`

- Sends a post request in order to modify a Movie
- Request Arguments: `id` - integer
- Request Body:

```json
{
    "title": "Updated title 1",
    "release_date": "01-Jan-2026"
}
```
- Returns: A list containing the modified Movie, in case of success
```json
{
    "movies": [
        {
            "id": 17,
            "release_date": "Tue, 31 Dec 2025 23:00:00 GMT",
            "title": "Updated title 1"
        }
    ],
    "success": true
}
```
---

`PATCH '/actors/${id}'`

- Sends a post request in order to modify an Actor
- Request Arguments: `id` - integer
- Request Body:

```json
{
    "name": "Marco Milani",
    "age": 42,
    "gender": "M"
}
```
- Returns: A list containing the modified Movie, in case of success
```json
{
    "actors": [
        {
            "age": 42,
            "gender": "M",
            "id": 31,
            "name": "Marco Milani"
        }
    ],
    "success": true
}
```
---

## Auth0 Setup:

**AUTH0_DOMAIN**, **ALGORITHMS** and **API_AUDIENCE** are all available in the `setup.sh` file for reference.

**Json Web Tokens**: You can find **JWTs** for each role in the `setup.sh` file to run the app locally.

**Roles**: The following roles have been defined in Auth0 with below permissions for each role.

- **Casting Assistant**
  - get:actors 
  - get:movies


- **Casting Director**
  - All permissions a Casting Assistant has
  - post:actors 
  - delete:actors
  - patch:actors 
  - patch:movies


- **Executive Producer**
  - All permissions a Casting Director has
  - post:movies 
  - delete:movies

## Deployment Details:

- App is deployed to [Render](https://harsh-casting-agency.herokuapp.com/ "Render").
- Render Postgres **DATABASE** details are available in `setup.sh` file for reference.

Use the above stated endpoints and append to this link above to execute the app either through CURL or Postman.

```bash
$ curl -X GET https://harsh-casting-agency.herokuapp.com/actors
$ curl -X POST https://harsh-casting-agency.herokuapp.com/actors
$ curl -X PATCH https://harsh-casting-agency.herokuapp.com/actors/1
$ curl -X DELETE https://harsh-casting-agency.herokuapp.com/actors/1
$ curl -X GET https://harsh-casting-agency.herokuapp.com/movies
$ curl -X POST https://harsh-casting-agency.herokuapp.com/movies
$ curl -X PATCH https://harsh-casting-agency.herokuapp.com/movies/1
$ curl -X DELETE https://harsh-casting-agency.herokuapp.com/movies/1
```

## Testing:

We can run our entire test case by running the following command at command line

```python
$ dropdb agency
$ createdb agency
$ psql agency < db.psql
$ python test_app.py
```

### Thank You!

import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import models
import auth
import logging
from logging import FileHandler, Formatter

from models import db_drop_and_create_all, setup_db, Actor, Movie
from auth import AuthError, requires_auth


# create and configure the app
app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

# Set up logging
error_log = FileHandler('error.log')
error_log.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
error_log.setLevel(logging.INFO)
app.logger.setLevel(logging.INFO)
app.logger.addHandler(error_log)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET, PATCH, POST, DELETE, OPTIONS')
    return response


# ROUTES
'''
Endpoint: /
Auth: None
Arguments: None
Returns: hello world (string)
Expected Success Code: 200
'''


@app.route('/', methods=['GET'])
def home():

    return jsonify({
        'success': True,
        'message': 'hello world'
    })


'''
Endpoint: /actors
Auth: get:actors
Arguments: None
Returns: List of actors
Expected Success Code: 200
'''


@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(jwt):
    actors = Actor.query.all()
    actorList = [actor.get_movie_info() for actor in actors]

    return jsonify({
        'success': True,
        'actors': actorList
    })


'''
Endpoint: /movies
Auth: get:movies
Arguments: None
Returns: List of movies
Expected Success Code: 200
'''


@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(jwt):
    movies = Actor.query.all()
    movieList = [movie.get_movie_info() for movie in movies]

    return jsonify({
        'success': True,
        'movies': movieList
    })


'''
Endpoint: /actors
Auth: post:actors
Arguments: None
Returns: Newly created actor
Expected Success Code: 200
'''


@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def create_actor(jwt):
    data = request.get_json()

    if 'name' and 'age' and 'gender' not in data:
        abort(422)

    name = data['name']
    age = data['age']
    gender = data['gender']

    actor = Actor(name=name, age=age, gender=gender)

    actor.insert()

    return jsonify({
        'success': True,
        'actor': actor.get_actor_info()
    })


'''
Endpoint: /movies
Auth: post:movies
Arguments: None
Returns: Newly created movie
Expected Success Code: 200
'''


@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def create_movie(jwt):
    data = request.get_json()

    if 'title' not in data:
        abort(422)

    title = data['title']
    movie = Movie(title=title)

    if 'release_date' in data:
        movie = Movie(title=title, release_date=data['release_date'])

    movie.insert()

    return jsonify({
        'success': True,
        'movie': movie.get_movie_info()
    })


'''
Endpoint: /actors/<actor id>
Auth: patch:actors
Arguments: Integer of actor ID
Returns: Array with updated actor information
Expected Success Code: 200
Failure: 404. actor of specified ID was not found
'''


@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(jwt, actor_id):
    actor = Actor.query.get(actor_id)

    if actor is None:
        abort(404)

    data = request.get_json()

    if 'name' in data:
        actor.name = data['name']

    if 'age' in data:
        actor.name = data['age']

    if 'gender' in data:
        actor.name = data['gender']

    if 'movie_id' in data:
        actor.name = data['movie_id']

    actor.update()

    return jsonify({
        'success': True,
        'drinks': [actor.get_actor_info()]
    })


'''
Endpoint: /movies/<movie id>
Auth: patch:movies
Arguments: Integer of movie ID
Returns: Array with updated movie information
Expected Success Code: 200
Failure: 404. movie of specified ID was not found
'''


@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(jwt, movie_id):
    movie = Movie.query.get(movie_id)

    if movie is None:
        abort(404)

    data = request.get_json()

    if 'title' in data:
        movie.title = data['title']

    if 'release_date' in data:
        movie.name = data['release_date']

    movie.update()

    return jsonify({
        'success': True,
        'drinks': [movie.get_movie_info()]
    })


'''
Endpoint: /actors/<actor id>
Auth: delete:actors
Arguments: Integer of actor ID
Returns: ID of deleted actor
Expected Success Code: 200
Failure: 404. actor of specified ID was not found
'''


@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(jwt, actor_id):
    actor = Actor.query.get(actor_id)

    if actor is None:
        abort(404)

    actor.delete()

    return jsonify({
        'success': True,
        'delete': actor.id
    })


'''
Endpoint: /movies/<movie id>
Auth: delete:movies
Arguments: Integer of movie ID
Returns: ID of deleted movie
Expected Success Code: 200
Failure: 404. movie of specified ID was not found
'''


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(jwt, movie_id):
    movie = Movie.query.get(movie_id)

    if movie is None:
        abort(404)

    movie.delete()

    return jsonify({
        'success': True,
        'delete': movie.id
    })


'''
Error handler for 422
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
Error handler for 404
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
Error handler for 401
'''


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorized"
    }), 401


'''
Error handler for 400
'''


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


'''
AuthError handler
'''


@app.errorhandler(AuthError)
def process_AuthError(error):
    response = jsonify(error.error)
    response.status_code = error.status_code

    return response

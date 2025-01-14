import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import setup_db, Actor, Movie, db
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.app_context().push()

    # migrate = Migrate(app, db)
    # migrate.init_app(app, db)

    setup_db(app)

    CORS(app)


    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PATCH, DELETE')
        return response

    # ---------------------------------------------------------------------------- #
    # Route Handlers
    # ---------------------------------------------------------------------------- #

    # root route, to check service health status
    @app.route('/')
    def check_status():
        return jsonify({
            'status': 'healthy'
        })

    # Retrieve movies list
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def retrieve_movies(payload):
        movies = Movie.query.order_by(Movie.id).all()

        if len(movies) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        }), 200

    # Retrieve actors list
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def retrieve_actors(payload):
        actors = Actor.query.order_by(Actor.id).all()

        if len(actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        }), 200

    # Delete a movie
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        try:
            if movie is None:
                abort(404)

            try:
                movie.delete()

                return jsonify({
                    "success": True,
                    "deleted_id": movie_id
                }), 200
            except:
                abort(400)
        except Exception as e:
            abort(e.code)

    # Delete an actor
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        try:
            if actor is None:
                abort(404)

            try:
                actor.delete()

                return jsonify({
                    "success": True,
                    "deleted_id": actor_id
                }), 200
            except:
                abort(400)
        except Exception as e:
            abort(e.code)

    # Create a new movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movies')
    def create_movie(payload):
        body = request.get_json()

        if 'title' not in body or 'release_date' not in body:
            abort(422)

        try:
            try:
                movie = Movie(title=body['title'], release_date=body['release_date'])
                movie.insert()

                return jsonify({
                    'success': True,
                    'movies': [movie.format()]
                }), 201
            except:
                abort(400)
        except Exception as e:
            abort(e.code)

    # Create a new actor
    @app.route('/actors', methods=['POST'])
    @requires_auth('create:actors')
    def create_actor(payload):
        body = request.get_json()

        if 'name' not in body or 'gender' not in body:
            abort(422)

        try:
            try:
                actor = Actor(name=body['name'], age=body['age'], gender=body['gender'])
                actor.insert()

                return jsonify({
                    'success': True,
                    'actors': [actor.format()]
                }), 201
            except:
                abort(400)
        except Exception as e:
            abort(e.code)

    # Update a movie
    @app.route('/movies/<int:movie_id>', methods=["PATCH"])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        body = request.get_json()
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        try:
            title = body.get('title')
            release_date = body.get('release_date')

            if title is not None:
                movie.title = title
            if release_date is not None:
                movie.release_date = release_date

            movie.update()

            return jsonify({
                'success': True,
                'movies': [movie.format()]
            }), 200
        except:
            abort(400)

    # Update an actor
    @app.route('/actors/<int:actor_id>', methods=["PATCH"])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        body = request.get_json()
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        try:
            name = body.get('name')
            age = body.get('age')
            gender = body.get('gender')

            if name is not None:
                actor.name = name
            if age is not None:
                actor.age = age
            if gender is not None:
                actor.gender = gender

            actor.update()

            return jsonify({
                'success': True,
                'actors': [actor.format()]
            }), 200
        except:
            abort(400)

    # ---------------------------------------------------------------------------- #
    # Error Handlers
    # ---------------------------------------------------------------------------- #
    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({
                'success': False,
                'error': 400,
                'message': 'Bad request'
            }), 400
        )

    @app.errorhandler(404)
    def bad_request(error):
        return (
            jsonify({
                'success': False,
                'error': 404,
                'message': 'Not found'
            }), 404
        )


    @app.errorhandler(401)
    def unauthorized(error):
        return (
            jsonify({
                'success': False,
                'error': 401,
                'message': 'Unauthorized'
            }), 401
        )

    @app.errorhandler(422)
    def unprocessed(error):
        return (
            jsonify({
                'success': False,
                'error': 422,
                'message': 'request cannot be processed'
            }), 422
        )

    @app.errorhandler(500)
    def generic_error(error):
        return (
            jsonify({
                'success': False,
                'error': 500,
                'message': 'Generic internal server error'
            }), 500
        )

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

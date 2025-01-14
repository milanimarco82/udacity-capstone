import os
import unittest
import json
import warnings

from flask_sqlalchemy import SQLAlchemy

import app
from app import create_app
from models import setup_db, Actor, Movie


class AgencyTestCase(unittest.TestCase):

    ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1VUHpmNUFldEpfdkx5UEdzUTJYcCJ9.eyJpc3MiOiJodHRwczovL2Rldi1ldjE3NjZxdTV0cGY2M21rLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzgwZGM4ODNlYWFiMWQ4MTE2MzM2YjQiLCJhdWQiOiJhZ2VuY3kiLCJpYXQiOjE3MzY4NTk5MTUsImV4cCI6MTczNjg2NzExNSwic2NvcGUiOiIiLCJhenAiOiJTRU4xOUNuN0VMazdtRVNrVHluNjJmaURna0ZTZ3dLVCIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.v5oOfcocbviP6XIkrYnNmq7TE5YG-PBXsGeJJaPeSHXc5z6ck5t_-CI0xOyDELXegOuTV7PXQ6k-aDyKnIYhjFKeptip2wzWTWQJPwniSN7hkDF1UcwJEX4lxP3BR8lgo3v-2rpNfQ-fTAE06Xst6dSo_hLXakXP4NzkT6tHn27U2wpzr7P7i6GI9ToNTW6utxTunaboyRn0C-yO72UznAw2eHBofRRXup8SULaqgSiiEGMQgP0hQbAFteUc2HvTS2yJK3GFsygOM3LIyUPXAnLeEo_XNXTGGo132h2rG5AoSeAkG7O7Fm4d_djjocPJr-1EEOIcO7x4ucV0uqYuDw'
    DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1VUHpmNUFldEpfdkx5UEdzUTJYcCJ9.eyJpc3MiOiJodHRwczovL2Rldi1ldjE3NjZxdTV0cGY2M21rLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzgwZGNjZWEyYTdjMjliMGZkMjAzODEiLCJhdWQiOiJhZ2VuY3kiLCJpYXQiOjE3MzY4NTk4NzAsImV4cCI6MTczNjg2NzA3MCwic2NvcGUiOiIiLCJhenAiOiJTRU4xOUNuN0VMazdtRVNrVHluNjJmaURna0ZTZ3dLVCIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvcnMiLCJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiXX0.Acycmcq_j6Io9m7G649wlsXWMfqjdGjJb8R75KV_AGaY5ACHfk-73ctG4xzp9ALJrJMtDP05rQBp6RukArTIYCr_tTNFDaJDdHeKvQPIE6kuLXl4UXQd10WVZF_5GkQu5ldZFmS0R7wPi8fb9b-kUlVz-s7HDP5QVq0WHRQEwfYHiEVrELp4ZvepZtzcAydW_H38N5zMsq8u3VzRUZom0z_kccNoozRxpJJlEMOiWFWAAFfuVatYVQCRouBJ14Xb83y2p26pF0xL59O2CF7VoHOiYVrIaTd2V-K7UcjCQcpWVroNJ1bu-Q-b3LEazhjn5ROMHD9WLZPaf7R33iVMVw'
    PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1VUHpmNUFldEpfdkx5UEdzUTJYcCJ9.eyJpc3MiOiJodHRwczovL2Rldi1ldjE3NjZxdTV0cGY2M21rLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzgwZGQwMGEyYTdjMjliMGZkMjAzZDUiLCJhdWQiOiJhZ2VuY3kiLCJpYXQiOjE3MzY4NTk5NzQsImV4cCI6MTczNjg2NzE3NCwic2NvcGUiOiIiLCJhenAiOiJTRU4xOUNuN0VMazdtRVNrVHluNjJmaURna0ZTZ3dLVCIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvcnMiLCJjcmVhdGU6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyJdfQ.ZmMyt2hr72rp3YNwXXEBLeh--2SPgEWAX7rvKikfet1HokGhTHRBbhmUhfq5j0EcdxsMIWlpc4NaFBahI9JJg4bK5ZAvfRi1bNKxY4FS9VWVcBMClPnjTZ430tzwkWknFmGSmaX2e-SZaoRv-9Ka1BdDblUgdlWeAUdwjcLVBNKU1Yx7UYT5ttLJH4UTVVWRZ03zJ3ofSwl3YiPdPdDf0zejvNbUr8Wn0MXkgJmxRddhbI53wfR6xvwcpgmQAeKxiUsc1NtctAaCRPz2OYYJpFhkqX7edBY5xF_Os97vTD6tQXPlLlMYO-YnukAAqFyCFLOOMNo1Tcv2uG1GerZWLg'

    def setUp(self):
        warnings.simplefilter('ignore', category=DeprecationWarning)
        # Define test variables and initialize app.

        self.database_path = os.getenv('TEST_DATABASE_URL', None)

        self.app = create_app()
        self.client = self.app.test_client

        setup_db(self.app, self.database_path)

        # JWT for different roles

        self.assistant_auth_header = {'Authorization':
                                      'Bearer ' + self.ASSISTANT_TOKEN}
        self.director_auth_header = {'Authorization':
                                     'Bearer ' + self.DIRECTOR_TOKEN}
        self.producer_auth_header = {'Authorization':
                                     'Bearer ' + self.PRODUCER_TOKEN}

        # JSON for objects creation/modification
        self.new_movie = {"title": "Test Movie", "release_date": "01-Jan-2025"}
        self.new_movie_no_title = {"release_date": "01-Jan-2025"}
        self.update_movie = {"release_date": "01-Jan-2026"}

        self.new_actor = {"name": "John Doe", "age": 40, "gender": "M"}
        self.new_actor_no_name = {"age": 40, "gender": "M"}
        self.update_actor = {"age": 99, "gender": "F"}

    def tearDown(self):
        pass

    # Check Health status
    def test_get_health_status(self):
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], "healthy")

    # Get Actors list (Assistant role)
    def test_get_actors_ass(self):
        res = self.client().get('/actors', headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # Get Movies list (Assistant role)
    def test_get_movies_ass(self):
        res = self.client().get('/movies', headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # Get Actors list (Director role)
    def test_get_actors_dir(self):
        res = self.client().get('/actors', headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # Get Actors list (Producer role)
    def test_get_actors_prod(self):
        res = self.client().get('/actors', headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # Get Movies list (Producer role)
    def test_get_movies_prod(self):
        res = self.client().get('/movies', headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # Delete Actor (Director role)
    def test_delete_actor_dir(self):
        first_actor = Actor.query.first()
        actor_id = first_actor.id
        res = self.client().delete('/actors/' + str(actor_id), headers=self.director_auth_header)
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], actor_id)
        self.assertTrue(data['deleted_id'])
        self.assertEqual(actor, None)

    # Error Delete Actor (not found - Director role)
    def test_error_delete_actor_dir(self):
        first_actor = Actor.query.first()
        actor_id = first_actor.id - 1
        res = self.client().delete('/actors/' + str(actor_id), headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # Create Actor (Director role)
    def test_create_actor_dir(self):
        res = self.client().post('/actors', json=self.new_actor, headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # Create Actor error (No name - Director role)
    def test_create_actor_err_dir(self):
        res = self.client().post('/actors', json=self.new_actor_no_name, headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # Create Actor error (Authorization - Assistant role)
    def test_create_actor_err_ass(self):
        res = self.client().post('/actors', json=self.new_actor, headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # Create Movie (Producer role)
    def test_create_movie_prod(self):
        res = self.client().post('/movies', json=self.new_movie, headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # Create Movie error (No title - Producer role)
    def test_create_movie_err_prod(self):
        res = self.client().post('/movies', json=self.new_movie_no_title, headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # Create Movie error (Authorization - Director role)
    def test_create_movie_err_dir(self):
        res = self.client().post('/movies', json=self.new_movie, headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # Delete Movie (Producer role)
    def test_delete_movie_prod(self):
        first_movie = Movie.query.first()
        movie_id = first_movie.id
        res = self.client().delete('/movies/' + str(movie_id), headers=self.producer_auth_header)
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], movie_id)
        self.assertTrue(data['deleted_id'])
        self.assertEqual(movie, None)

    # Error Delete Movie (not found - Producer role)
    def test_error_delete_movie_prod(self):
        first_movie = Movie.query.first()
        movie_id = first_movie.id - 1
        res = self.client().delete('/movies/' + str(movie_id), headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # Modify Actor (Director role)
    def test_update_actor_dir(self):
        first_actor = Actor.query.first()
        actor_id = first_actor.id
        res = self.client().patch('/actors/' + str(actor_id), json=self.update_actor, headers=self.director_auth_header)
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # Modify Actor (Not found - Director role)
    def test_error_update_actor_dir(self):
        first_actor = Actor.query.first()
        actor_id = first_actor.id - 1
        res = self.client().patch('/actors/' + str(actor_id), json=self.update_actor, headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # Modify Actor (Authorization - Assistant role)
    def test_error_update_actor_ass(self):
        first_actor = Actor.query.first()
        actor_id = first_actor.id
        res = self.client().patch('/actors/' + str(actor_id), json=self.update_actor, headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # Modify Movie (Producer role)
    def test_update_movie_prod(self):
        first_movie = Movie.query.first()
        movie_id = first_movie.id
        res = self.client().patch('/movies/' + str(movie_id), json=self.update_movie, headers=self.producer_auth_header)
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # Modify Movie (Not found - Producer role)
    def test_error_update_movie_prod(self):
        first_movie = Movie.query.first()
        movie_id = first_movie.id - 1
        res = self.client().patch('/movies/' + str(movie_id), json=self.update_movie, headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # Modify Movie (Authorization - Assistant role)
    def test_error_update_movie_ass(self):
        first_movie = Movie.query.first()
        movie_id = first_movie.id
        res = self.client().patch('/movies/' + str(movie_id), json=self.update_movie, headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
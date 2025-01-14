import os
import unittest
import json
import warnings

from flask_sqlalchemy import SQLAlchemy

import app
from app import create_app
from models import setup_db, Actor, Movie


class AgencyTestCase(unittest.TestCase):

    ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1VUHpmNUFldEpfdkx5UEdzUTJYcCJ9.eyJpc3MiOiJodHRwczovL2Rldi1ldjE3NjZxdTV0cGY2M21rLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzgwZGM4ODNlYWFiMWQ4MTE2MzM2YjQiLCJhdWQiOiJhZ2VuY3kiLCJpYXQiOjE3MzY4NzU1NjYsImV4cCI6MTczNjk2MTk2Niwic2NvcGUiOiIiLCJhenAiOiJTRU4xOUNuN0VMazdtRVNrVHluNjJmaURna0ZTZ3dLVCIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.s7kD71uDbtRyIql1JQgz4re01TmcnxZgBrHPKTIBvrVubaNFssEXbLB4njpEs9Zu_2k6-01AbwPDp9VrRDfT99WejUV3VCYpVrxNmclf88Em1ZFF3Cl_Rb4A3zW2HVQtpjrDKRXcET8qjjs_Hv3-MTscC0kw-1_qpVCPL0wAbYP7yRdTjfv9v-OzsS51S6U58hYwzjJmELHHLa_JT-CzABDeEU7PJtv0il0NHQDl8tl_889P1owXSQ1NKgNMYD-RRGyW1WasZ1iS994qXez5UFdAUbJWd1_5X21_POWZTNIfbzQVBiTuv30cHZxTzHTBvT0RVi-Zf5kghxIjaZKbGQ'
    DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1VUHpmNUFldEpfdkx5UEdzUTJYcCJ9.eyJpc3MiOiJodHRwczovL2Rldi1ldjE3NjZxdTV0cGY2M21rLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzgwZGNjZWEyYTdjMjliMGZkMjAzODEiLCJhdWQiOiJhZ2VuY3kiLCJpYXQiOjE3MzY4NzU1MzMsImV4cCI6MTczNjk2MTkzMywic2NvcGUiOiIiLCJhenAiOiJTRU4xOUNuN0VMazdtRVNrVHluNjJmaURna0ZTZ3dLVCIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvcnMiLCJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiXX0.q-9Rv6KVgcW18_VMriAwwmfZgrSe6X5beATsIGJjRO3DO1IRsJrKZqXvcH7PPOmnOu0M22soHdlVoXBX7z0D8fl9pgfUdUaPpNRgv4l7qvutl1-ps9ObxVpjre7jzxBXYHqWVJOnFmBEirSSgKa4a39KCSQvVRab__uWoeD3uUIJOqN0FV_zc-Eqqy3WjhX3DTZaBFMwk2PIFvORNL3AlS9MmgcplrLeXwJeveDkTaVFKKocWn0i3Som_aQ6CZwzJexLvJdJzDt1sfgG_OMl2oZ0yma30YxQiXkTik2J8i0wZC_-NC9bHvCu8C4n7vsFC6sar6wX-S6wRTXDy5Q1rg'
    PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1VUHpmNUFldEpfdkx5UEdzUTJYcCJ9.eyJpc3MiOiJodHRwczovL2Rldi1ldjE3NjZxdTV0cGY2M21rLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzgwZGQwMGEyYTdjMjliMGZkMjAzZDUiLCJhdWQiOiJhZ2VuY3kiLCJpYXQiOjE3MzY4NzU1OTgsImV4cCI6MTczNjk2MTk5OCwic2NvcGUiOiIiLCJhenAiOiJTRU4xOUNuN0VMazdtRVNrVHluNjJmaURna0ZTZ3dLVCIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvcnMiLCJjcmVhdGU6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyJdfQ.WuzpewkN0IXZI1mDjMxYNR4PBgOUfUG6BRwTjgtsFhcySGb_NUvD-aewEeWmQE4YzvRo29EgjFVttoBk_dt4_cxqyCy9DQElONtmxdOqfbl684HoM2g5Zrodqq5LPwRCb-GFEE0XYuNsoGQb23ySWrWb2D_M3WzvldGXI6VEppVxSGyf4F16emwIRe02GaDLDVOEc6YYtU8Eyz48nX1UEY04Or_81jT7IF5DCc_qUE7ox58DcPiHMv8lQiosUBLk13Nj4Sm-iv8qYtp-UO8EJ2vIqIwZFWvxvO0NoszNH90TWfxmOIpUcskY4xsf1cs68jCJMiRUIvWPF5YlpXasog'

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

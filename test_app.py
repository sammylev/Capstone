import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import app
from models import db,db_drop_and_create_all, setup_db, Movie, Actor
from auth import AuthError, requires_auth
from sqlalchemy import Column, String, Integer, DateTime
import logging


database_name = "database_test.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_name))

assistant_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlF6RkJPRVEzTkRFME5UZEJSVVpGUXprek5UVkRSVUV3UWtNMlFqVkRSRU5ETWprMFJETXlNQSJ9.eyJpc3MiOiJodHRwczovL2Rldi1zYW1teWxldi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU0YjdjNGNlN2NkMDEwZWZlOWRiMDRhIiwiYXVkIjoiY2FzdGluZ2FwcCIsImlhdCI6MTU4MzY0NTY3MiwiZXhwIjoxNTg0ODU1MjcyLCJhenAiOiJtTXEyMjRXOTk4dVNjVTR2eTJ1YjVJdmhmQ1V2c0xkMSIsImd0eSI6InBhc3N3b3JkIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.kTofgR6RZcWbM9SG5Yu2GUgbe-rSyZLnDVFwLuqie2JtyntWYz4WtuSYJDL2gQSpD-nKtD6V1E0GnsbIpvKiF2fsomyRtBwyo-GgI9qcBF71Qj09wD2uEipFlLm-AH-oBv-8MmwaDlZHe3io5R3HjUHOVEaq8s0Q9a1HeBUfQUtyO70xit9122ZCKlyWqkbbs2GacoY8XyyiHAHdo8dSlcN6_YzTyf_TrRywzxPCj1G7yZL4cPc1Qr5g0XlBS1BnHKPPlxCf-bgSHwE6ZIwMHsIMhBIop1kW_h-WbmiBLPgBXkZJJSZ4Kn7No4R_04_VPTd7nP81x-4Rn43FaOdQLA"
director_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlF6RkJPRVEzTkRFME5UZEJSVVpGUXprek5UVkRSVUV3UWtNMlFqVkRSRU5ETWprMFJETXlNQSJ9.eyJpc3MiOiJodHRwczovL2Rldi1zYW1teWxldi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU0YjdjN2I2NmE2ZDkwZWQwYjM2MzkzIiwiYXVkIjoiY2FzdGluZ2FwcCIsImlhdCI6MTU4MzY0NTgxNSwiZXhwIjoxNTg0ODU1NDE1LCJhenAiOiJtTXEyMjRXOTk4dVNjVTR2eTJ1YjVJdmhmQ1V2c0xkMSIsImd0eSI6InBhc3N3b3JkIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.W3e4bMsqSX5W08CwV3Nce3lZh579tI5dYTWfkuPvn_lPWT8VuQX5oY5TIhPhQQIaVhyB0vNG63o60GqPJhmIng4YEZsU39nsMlcYmgzd090vLOYqJE5U0XfeTYICNYLO-aHRirGdj_3Arw1nkUoAPvXgjTKiJL0hAjMBDb28F5z55S7ckP9EDydO6yvd_mJzsQlOwSr6YvJCecUI7HNzC8jHYqmIvWS9kR5u27MUbXmwhixkEtQKXnJGVlqn77uPLl8SWyjGSWyoNArAKQLEdix7iqF5n_tKhu4BbUlWdjzYX6Dp8O3RIAciWqsHgmn7tj4-6aJbNpo88QdkMcfT4A"
producer_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlF6RkJPRVEzTkRFME5UZEJSVVpGUXprek5UVkRSVUV3UWtNMlFqVkRSRU5ETWprMFJETXlNQSJ9.eyJpc3MiOiJodHRwczovL2Rldi1zYW1teWxldi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU0YjdjYzdmZTUyYWMwZjU2NmY4NDhmIiwiYXVkIjoiY2FzdGluZ2FwcCIsImlhdCI6MTU4MzY0NTg5NiwiZXhwIjoxNTg0ODU1NDk2LCJhenAiOiJtTXEyMjRXOTk4dVNjVTR2eTJ1YjVJdmhmQ1V2c0xkMSIsImd0eSI6InBhc3N3b3JkIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.QFLWTA0nerUCUfIjb7nOHiWhsuOTcru1af84paIYHyi5hB5KMwQbrz4EuENbDHiiSVHFXM4zngG-6KuvuPPdFY5HPIoG-Em0ZOwDUpCC85ymVtfep7iP9BXlgx2zvtnZBkU2AnIZihDzKWpnCgSYvyMcIsRBbqLGsPJxKYsE7raXBRmuIQ6pY3r6smEwqxn44HC1yL8aYoLeONZJAOY8my5eVaq1k-RNi27hczT_qtYm-YC94D5n1Zg4tSPo6jB1UoGhj5MpP_zTumvYhrvYd4DY_Fh8WxxBUowaRerIKhagMruLXBwbOTqhF4gtqjZMqibp1qB_UmuRxdJnh-BMFw"

def set_auth(role):
    if role == 'assistant':
        return {"Content-Type": "application/json","Authorization": "Bearer {}".format(assistant_token)}
    elif role == 'director':
        return {"Content-Type": "application/json",'Authorization': 'Bearer {}'.format(director_token)}
    elif role == 'producer':
        return {"Content-Type": "application/json",'Authorization': 'Bearer {}'.format(producer_token)}

class testCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = database_path
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_movies_assistant(self):
        res = self.app.get('/movies', headers=set_auth('assistant'))
        self.assertEqual(res.status_code, 200)

    def test_get_movies_director(self):
        res = self.app.get('/movies', headers=set_auth('director'))
        self.assertEqual(res.status_code, 200)

    def test_get_movies_producer(self):
        res = self.app.get('/movies', headers=set_auth('producer'))
        self.assertEqual(res.status_code, 200)

    def test_get_movies_fail(self):
        res = self.app.get('/movies', headers=set_auth(''))
        self.assertEqual(res.status_code, 401)

    def test_post_movie_assistant(self):
        data = {
            "title": "test_title"
        }
        res = self.app.post('/movies', json=data, headers=set_auth('assistant'))
        self.assertEqual(res.status_code, 401)

    def test_post_movie_director(self):
        data = {
            "title": "test_title"
        }
        res = self.app.post('/movies', json=data, headers=set_auth('director'))
        self.assertEqual(res.status_code, 401)

    def test_post_movie_producer(self):
        data = {
            "title": "test_title"
        }
        res = self.app.post('/movies', json=data, headers=set_auth('producer'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    def test_post_movie_fail(self):
        res = self.app.post('/movies', json={}, headers=set_auth('producer'))
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res.get_json()['success'], False)

    def test_patch_movie_assistant(self):
        data = {
            "title": "test_title"
        }
        res = self.app.post('/movies', json=data, headers=set_auth('producer'))

        updated_data = {
            "title": "updated_title"
        }

        res = self.app.patch('/movies/1', json=updated_data, headers=set_auth('assistant'))
        self.assertEqual(res.status_code, 401)

    def test_patch_movie_director(self):
        data = {
            "title": "test_title"
        }
        res = self.app.post('/movies', json=data, headers=set_auth('producer'))

        updated_data = {
            "title": "updated_title"
        }

        res = self.app.patch('/movies/1', json=updated_data, headers=set_auth('director'))
        self.assertEqual(res.status_code, 200)

    def test_patch_movie_producer(self):
        data = {
            "title": "test_title"
        }
        res = self.app.post('/movies', json=data, headers=set_auth('producer'))

        updated_data = {
            "title": "updated_title"
        }

        res = self.app.patch('/movies/1', json=updated_data, headers=set_auth('producer'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    def test_patch_movie_fail(self):
        data = {
            "title": "test_title"
        }
        res = self.app.post('/movies', json=data, headers=set_auth('producer'))

        res = self.app.patch('/movies/100000', json={}, headers=set_auth('producer'))

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.get_json()['success'], False)

    def test_delete_movie_fail(self):
        res = self.app.delete('/movies/1000000', headers=set_auth('producer'))
        self.assertEqual(res.status_code, 404)

    def test_delete_movie_assistant(self):
        data = {
            "title": "test_title"
        }
        res = self.app.post('/movies', json=data, headers=set_auth('producer'))

        res = self.app.delete('/movies/1', headers=set_auth('assistant'))
        self.assertEqual(res.status_code, 401)


    def test_delete_movie_director(self):
        data = {
            "title": "test_title"
        }
        res = self.app.post('/movies', json=data, headers=set_auth('producer'))

        res = self.app.delete('/movies/1', headers=set_auth('director'))
        self.assertEqual(res.status_code, 401)


    def test_delete_movie_producer(self):
        data = {
            "title": "test_title"
        }
        res = self.app.post('/movies', json=data, headers=set_auth('producer'))

        res = self.app.delete('/movies/1', headers=set_auth('producer'))
        self.assertEqual(res.status_code, 200)

    def test_delete_movies_fail(self):
        res = self.app.delete('/movies/1', headers=set_auth(''))
        self.assertEqual(res.status_code, 401)

    #Actor Tests
    def test_get_actors_assistant(self):
        res = self.app.get('/actors', headers=set_auth('assistant'))
        self.assertEqual(res.status_code, 200)

    def test_get_actors_director(self):
        res = self.app.get('/actors', headers=set_auth('director'))
        self.assertEqual(res.status_code, 200)

    def test_get_actors_producer(self):
        res = self.app.get('/actors', headers=set_auth('producer'))
        self.assertEqual(res.status_code, 200)

    def test_get_actor_fail(self):
        res = self.app.get('/actors', headers=set_auth(''))
        self.assertEqual(res.status_code, 401)

    def test_post_actor_assistant(self):
        data = {
            "name": "updated_name",
            "gender": "female",
            "age": 30
        }
        res = self.app.post('/actors', json=data, headers=set_auth('assistant'))
        self.assertEqual(res.status_code, 401)

    def test_post_actor_director(self):
        data = {
            "name": "updated_name",
            "gender": "female",
            "age": 30
        }
        res = self.app.post('/actors', json=data, headers=set_auth('director'))
        self.assertEqual(res.status_code, 200)

    def test_post_actor_producer(self):
        data = {
            "name": "updated_name",
            "gender": "female",
            "age": 30
        }
        res = self.app.post('/actors', json=data, headers=set_auth('producer'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    def test_post_actors_fail(self):
        res = self.app.post('/actors', json={}, headers=set_auth('producer'))
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res.get_json()['success'], False)

    def test_patch_actor_assistant(self):
        data = {
            "name": "test_name",
            "gender": "female",
            "age": 30
        }
        res = self.app.post('/actors', json=data, headers=set_auth('producer'))

        updated_data = {
            "name": "updated_name",
            "gender": "female",
            "age": 35
        }

        res = self.app.patch('/actors/1', json=updated_data, headers=set_auth('assistant'))
        self.assertEqual(res.status_code, 401)

    def test_patch_actor_director(self):
        data = {
            "name": "test_name",
            "gender": "female",
            "age": 30
        }
        res = self.app.post('/actors', json=data, headers=set_auth('director'))

        updated_data = {
            "name": "updated_name",
            "gender": "female",
            "age": 35
        }

        res = self.app.patch('/actors/1', json=updated_data, headers=set_auth('director'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    def test_patch_actor_producer(self):
        data = {
            "name": "test_name",
            "gender": "female",
            "age": 30
        }
        res = self.app.post('/actors', json=data, headers=set_auth('producer'))

        updated_data = {
            "name": "updated_name",
            "gender": "female",
            "age": 35
        }

        res = self.app.patch('/actors/1', json=updated_data, headers=set_auth('producer'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    def test_patch_actor_fail(self):
        data = {
            "name": "test_name",
            "gender": "female",
            "age": 30
        }
        res = self.app.post('/actors', json=data, headers=set_auth('producer'))

        res = self.app.patch('/actors/100000', json={}, headers=set_auth('producer'))

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.get_json()['success'], False)

    def test_delete_actor_assistant(self):
        data = {
            "name": "test_name",
            "gender": "female",
            "age": 30
        }
        res = self.app.post('/actors', json=data, headers=set_auth('assistant'))

        res = self.app.delete('/actors/1', headers=set_auth('assistant'))
        self.assertEqual(res.status_code, 401)

    def test_delete_actor_director(self):
        data = {
            "name": "test_name",
            "gender": "female",
            "age": 30
        }
        res = self.app.post('/actors', json=data, headers=set_auth('director'))

        res = self.app.delete('/actors/1', headers=set_auth('director'))
        self.assertEqual(res.status_code, 200)

    def test_delete_actor_producer(self):
        data = {
            "name": "test_name",
            "gender": "female",
            "age": 30
        }
        res = self.app.post('/actors', json=data, headers=set_auth('producer'))

        res = self.app.delete('/actors/1', headers=set_auth('producer'))
        self.assertEqual(res.status_code, 200)

    def test_delete_actor_fail(self):
        logging.info("Intentionally Missing Auth Header (see below)")
        res = self.app.delete('/actors/1', headers=set_auth(''))
        self.assertEqual(res.status_code, 401)

if __name__ == '__main__':
    unittest.main()
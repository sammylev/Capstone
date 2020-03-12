import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import app
from models import db, db_drop_and_create_all, setup_db, Movie, Actor
from auth import AuthError, requires_auth
from sqlalchemy import Column, String, Integer, DateTime
import logging
from configparser import ConfigParser


database_name = "database_test.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_name))

assistant_token = os.getenv('ASSISTANT_JWT')
director_token = os.getenv('DIRECTOR_JWT')
producer_token = os.getenv('PRODUCER_JWT')


def set_auth(role):
    if role == 'assistant':
        return {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(assistant_token)
            }
    elif role == 'director':
        return {
            "Content-Type": "application/json",
            'Authorization': 'Bearer {}'.format(director_token)
            }
    elif role == 'producer':
        return {
            "Content-Type": "application/json",
            'Authorization': 'Bearer {}'.format(producer_token)
            }


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
        res = self.app.post('/movies', json=data,
                            headers=set_auth('assistant'))
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

        res = self.app.patch('/movies/1', json=updated_data,
                             headers=set_auth('assistant'))
        self.assertEqual(res.status_code, 401)

    def test_patch_movie_director(self):
        data = {
            "title": "test_title"
        }
        res = self.app.post('/movies', json=data, headers=set_auth('producer'))

        updated_data = {
            "title": "updated_title"
        }

        res = self.app.patch('/movies/1', json=updated_data,
                             headers=set_auth('director'))
        self.assertEqual(res.status_code, 200)

    def test_patch_movie_producer(self):
        data = {
            "title": "test_title"
        }
        res = self.app.post('/movies', json=data, headers=set_auth('producer'))

        updated_data = {
            "title": "updated_title"
        }

        res = self.app.patch('/movies/1', json=updated_data,
                             headers=set_auth('producer'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    def test_patch_movie_fail(self):
        data = {
            "title": "test_title"
        }
        res = self.app.post('/movies', json=data, headers=set_auth('producer'))

        res = self.app.patch('/movies/100000', json={},
                             headers=set_auth('producer'))

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

    # Actor Tests
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
        res = self.app.post('/actors', json=data,
                            headers=set_auth('assistant'))
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

        res = self.app.patch('/actors/1', json=updated_data,
                             headers=set_auth('assistant'))
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

        res = self.app.patch('/actors/1', json=updated_data,
                             headers=set_auth('director'))
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

        res = self.app.patch('/actors/1', json=updated_data,
                             headers=set_auth('producer'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    def test_patch_actor_fail(self):
        data = {
            "name": "test_name",
            "gender": "female",
            "age": 30
        }
        res = self.app.post('/actors', json=data, headers=set_auth('producer'))

        res = self.app.patch('/actors/100000', json={},
                             headers=set_auth('producer'))

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.get_json()['success'], False)

    def test_delete_actor_assistant(self):
        data = {
            "name": "test_name",
            "gender": "female",
            "age": 30
        }
        res = self.app.post('/actors', json=data,
                            headers=set_auth('assistant'))

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

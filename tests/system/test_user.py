import json

from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            # with self.app_context():
                response = client.post('/register', data={'username': 'test_user', 'password': 'test_password'})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test_user'))
                self.assertDictEqual(json.loads(response.data.decode()), {'message': 'User created OK'})

    def test_login_user(self):
        with self.app() as client:
            # with self.app_context():
                client.post('/register', data={'username': 'test_user', 'password': 'test_password'})
                auth_resp = client.post('/auth',
                                        data=json.dumps({'username': 'test_user', 'password': 'test_password'}),
                                        headers={'Content-Type': 'application/json'})

                self.assertIn('access_token', json.loads(auth_resp.data.decode()).keys())


    def test_register_duplicate(self):
        with self.app() as client:
            # with self.app_context():
                client.post('/register', data={'username': 'test_user', 'password': 'test_password'})
                response = client.post('/register', data={'username': 'test_user', 'password': 'test_password'})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(json.loads(response.data.decode()),
                                     {'message': 'A user with that username already exist'})

    def test_user_delete(self):
        with self.app() as client:
            client.post('/register', data={'username': 'test_user', 'password': 'test_password'})

            self.assertIsNotNone(UserModel.find_by_username('test_user'))

            response = client.delete('/user/test_user')

            self.assertEqual(200, response.status_code)
            self.assertDictEqual({'message': 'user deleted'}, json.loads(response.data.decode()))
            self.assertIsNone(UserModel.find_by_username('test_user'))

    def test_user_delete_not_found(self):
        with self.app() as client:
            response = client.delete('/user/test_user')

            self.assertEqual(404, response.status_code)
            self.assertDictEqual({'message': 'no such user'}, json.loads(response.data.decode()))

    def test_user_list(self):
        with self.app() as client:
            client.post('/register', data={'username': 'test_user', 'password': 'test_password'})
            client.post('/register', data={'username': 'test_user2', 'password': 'test_password'})

            response = client.get('/users')

            self.assertDictEqual(
                {'users': [{'id': 1, 'username': 'test_user'}, {'id': 2, 'username': 'test_user2'}]},
                json.loads(response.data.decode())
            )

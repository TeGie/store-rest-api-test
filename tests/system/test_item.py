import json

from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test_user', 'test_password').save_to_db()
                auth_request = client.post('/auth',
                                           data=json.dumps({'username': 'test_user', 'password': 'test_password'}),
                                           headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data.decode())['access_token']
                self.access_token = 'JWT {}'.format(auth_token)

    def test_get_item_no_auth(self):
        with self.app() as client:
                resp = client.get('/item/test_item')

                self.assertEqual(401, resp.status_code)

    def test_get_item_not_found(self):
        with self.app() as client:
                    resp = client.get('/item/test_item', headers={'Authorization': self.access_token})

                    self.assertEqual(404, resp.status_code)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                ItemModel('test_item', 2.15, 1).save_to_db()

                resp = client.get('/item/test_item', headers={'Authorization': self.access_token})

                self.assertEqual(200, resp.status_code)
                self.assertDictEqual({'name': 'test_item', 'price': 2.15}, json.loads(resp.data.decode()))

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                # StoreModel('test_store').save_to_db()  # needed for non-sqlite databases
                ItemModel('test_item', 2.15, 1).save_to_db()

                resp = client.delete('/item/test_item')

                self.assertDictEqual({'message': 'Item deleted'}, json.loads(resp.data.decode()))
                self.assertEqual(200, resp.status_code)
                
    def test_delete_item_no_found(self):
        with self.app() as client:
            # StoreModel('tests_store')  # needed for non-sqlite databases
            resp = client.delete('/item/test_item')

            self.assertDictEqual({'message': 'No such item'}, json.loads(resp.data.decode()))
            self.assertEqual(404, resp.status_code)

    def test_create_item(self):
        with self.app() as client:
            resp = client.post('/item/test_item',
                               data=json.dumps({'price': 2.15, 'store_id': 1}),
                               headers={'Content-Type': 'application/json'})

            self.assertEqual(201, resp.status_code)
            self.assertDictEqual({'name': 'test_item', 'price': 2.15}, json.loads(resp.data.decode()))


    def test_create_item_duplicate(self):
        with self.app() as client:
            client.post('/item/test_item',
                        data=json.dumps({'price': 2.15, 'store_id': 1}),
                        headers={'Content-Type': 'application/json'})
            resp = client.post('/item/test_item',
                               data=json.dumps({'price': 2.15, 'store_id': 1}),
                               headers={'Content-Type': 'application/json'})

            self.assertEqual(400, resp.status_code)
            self.assertDictEqual({'message': "An item with name 'test_item' already exists."},
                                 json.loads(resp.data.decode()))

    def test_put_item(self):
        with self.app() as client:
            resp = client.put('/item/test_item',
                       data=json.dumps({'price': 2.15, 'store_id': 1}),
                       headers={'Content-Type': 'application/json'})

            self.assertEqual(200, resp.status_code)
            self.assertDictEqual({'name': 'test_item', 'price': 2.15}, json.loads(resp.data.decode()))

    def test_put_update_item(self):
        with self.app() as client:
            client.put('/item/test_item', data={'price': 2.15, 'store_id': 1}) #  no json.dumps and headers
            resp = client.put('/item/test_item', data={'price': 3.26, 'store_id': 1})

            self.assertEqual(200, resp.status_code)
            self.assertDictEqual({'name': 'test_item', 'price': 3.26}, json.loads(resp.data.decode()))

    def test_list_item(self):
        with self.app() as client:
            with self.app_context():
                ItemModel('test_item', 2.15, 1).save_to_db()
                ItemModel('test_item_2', 3.26, 2).save_to_db()

                resp = client.get('/items')

                self.assertEqual(200, resp.status_code)
                self.assertDictEqual(
                    {'items': [{'name': 'test_item', 'price': 2.15}, {'name': 'test_item_2', 'price': 3.26}]},
                    json.loads(resp.data.decode()))


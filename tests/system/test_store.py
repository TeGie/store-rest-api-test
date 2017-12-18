import json
# from unittest.mock import patch

from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store_message_and_status_code(self):
        with self.app() as client:
            resp = client.post('/store/test_store')

            self.assertEqual(201, resp.status_code)
            self.assertDictEqual({'id': 1, 'name': 'test_store', 'items': []}, json.loads(resp.data.decode()))
            self.assertIsNotNone(StoreModel.find_by_name('test_store'))

    # def test_create_store_calls_save_to_db(self):
    #     with patch('section7.starter_code.models.store.StoreModel.save_to_db') as patched_save:
    #         with self.app() as client:
    #             client.post('/store/test_store')
    #
    #             patched_save.assert_called_with()

    def test_create_duplicate_store_with_save_to_db(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()

                resp = client.post('/store/test_store')

                self.assertEqual(400, resp.status_code)
                self.assertDictEqual(
                    {'message': "A store with name 'test_store' already exists."},
                    json.loads(resp.data.decode())
                )

    # def test_create_duplicate_store_with_post(self):
    #     with self.app() as client:
    #         client.post('/store/test_store')
    #         resp = client.post('/store/test_store')
    #
    #         self.assertEqual(400, resp.status_code)
    #         self.assertDictEqual(
    #             {'message': "A store with name 'test_store' already exists."},
    #             json.loads(resp.data.decode())
    #         )

    def test_delete_store_message_and_status_code(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()

                resp = client.delete('/store/test_store')

                self.assertIsNone(StoreModel.find_by_name('test_store'))
                self.assertDictEqual({'message': 'Store deleted'}, json.loads(resp.data.decode()))
                self.assertEqual(200, resp.status_code)

    # def test_delete_store_calls_delete_from_db(self):
    #     with patch('section7.starter_code.models.store.StoreModel.delete_from_db') as mocked_delete:
    #         with self.app() as client:
    #             with self.app_context():
    #                 StoreModel('test_store').save_to_db()
    #                 client.delete('/store/test_store')
    #
    #                 mocked_delete.assert_called_with()

    def test_delete_store_not_found(self):
        with self.app() as client:
            resp = client.delete('/store/test_store')

            self.assertDictEqual({'message': 'No such store'}, json.loads(resp.data.decode()))
            self.assertEqual(404, resp.status_code)

    # def test_delete_store_not_found_with_post(self):
    #     with self.app() as client:
    #         client.post('/store/test_store_2')
    #         resp = client.delete('/store/test_store')
    #
    #         self.assertDictEqual({'message': 'No such store'}, json.loads(resp.data.decode()))
    #         self.assertEqual(404, resp.status_code)

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                resp = client.get('/store/test_store')

                self.assertDictEqual({'id': 1, 'name': 'test_store', 'items': []}, json.loads(resp.data.decode()))
                self.assertEqual(200, resp.status_code)

    def test_store_not_found(self):
        with self.app() as client:
            resp = client.get('/store/test_store')

            self.assertDictEqual({'message': 'Store not found'}, json.loads(resp.data.decode()))
            self.assertEqual(404, resp.status_code)

    # def test_store_not_found_with_post(self):
    #     with self.app() as client:
    #         client.post('/store/test_store_2')
    #         resp = client.get('/store/test_store')
    #
    #         self.assertDictEqual({'message': 'Store not found'}, json.loads(resp.data.decode()))
    #         self.assertEqual(404, resp.status_code)

    def test_store_found_with_items_with_save_to_db(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 2.15, 1).save_to_db()

                resp = client.get('/store/test_store')

                self.assertEqual(200, resp.status_code)
                self.assertDictEqual(
                    {'id': 1, 'name': 'test_store', 'items': [{'name': 'test_item', 'price': 2.15}]},
                    json.loads(resp.data.decode())
                )

    # def test_store_found_with_items_with_post(self):
    #     with self.app() as client:
    #         client.post('/store/test_store')
    #         ItemModel('test_item', 2.15, 1).save_to_db()
    #
    #         resp = client.get('/store/test_store')
    #
    #         self.assertEqual(200, resp.status_code)
    #         self.assertDictEqual(
    #             {'name': 'test_store', 'items': [{'name': 'test_item', 'price': 2.15}]},
    #             json.loads(resp.data.decode())
    #         )

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                StoreModel('test_store_2').save_to_db()

                resp = client.get('/stores')

                self.assertEqual(200, resp.status_code)
                self.assertDictEqual(
                    {'stores': [{'id': 1, 'name': 'test_store', 'items': []}, {'id': 2, 'name': 'test_store_2', 'items': []}]},
                    json.loads(resp.data.decode())
                )

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 2.15, 1).save_to_db()

                resp = client.get('/stores')

                self.assertEqual(200, resp.status_code)
                self.assertDictEqual(
                   {'stores': [{'id': 1, 'name': 'test_store', 'items': [{'name': 'test_item', 'price': 2.15}]}]},
                   json.loads(resp.data.decode())
                )

    def test_store_list_empty(self):
        with self.app() as client:

            resp = client.get('/stores')

            self.assertEqual(200, resp.status_code)
            self.assertDictEqual(
               {'stores': []},
               json.loads(resp.data.decode())
            )

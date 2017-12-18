from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel('test_store')

        self.assertListEqual(store.items.all(), [])

    def test_crud(self):
        with self.app_context():
            store = StoreModel('test_store')

            self.assertIsNone(StoreModel.find_by_name('test_store'))

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('test_store'))

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('test_store'))

    def test_store_items_relationship(self):
        with self.app_context():
            store = StoreModel('test_store')
            item = ItemModel('test_item', 2.15, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertListEqual(store.items.all(), [item])
            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'test_item')

    def test_store_json(self):
        store = StoreModel('test_store')

        expected = {
            'id': None,
            'name': 'test_store',
            'items': []
        }

        self.assertDictEqual(store.json(), expected)

    def test_store_json_with_items(self):
        with self.app_context():
            store = StoreModel('test_store')
            item = ItemModel('test_item', 2.15, 1)
            item2 = ItemModel('test_item2', 3.26, 1)

            expected = {
                'id': 1,
                'name': 'test_store',
                'items': [
                    {
                        'name': 'test_item',
                        'price': 2.15
                    },
                    {
                        'name': 'test_item2',
                        'price': 3.26
                    }
                ]
            }

            store.save_to_db()
            item.save_to_db()
            item2.save_to_db()

            self.assertDictEqual(store.json(), expected)

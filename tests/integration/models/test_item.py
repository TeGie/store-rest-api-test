from models.item import ItemModel
from tests.base_test import BaseTest
from models.store import StoreModel


class ItemTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            StoreModel('Test store').save_to_db() #for postgres, mysql because of foreign key constrains
            item = ItemModel('Test item', 2.15, 1)

            self.assertIsNone(ItemModel.find_by_name('Test item'),
                              "Found an item with name {}, but expected not to.".format(item.name))

            item.save_to_db()

            self.assertIsNotNone(ItemModel.find_by_name('Test item'))

            item.delete_from_db()

            self.assertIsNone(ItemModel.find_by_name('Test item'))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('Test store')
            item = ItemModel('Test item', 2.15, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual('Test store', item.store.name)
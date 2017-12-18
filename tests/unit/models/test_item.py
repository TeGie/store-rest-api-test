from models.item import ItemModel
from tests.unit.unit_base_test import UnitBaseTest


class ItemTest(UnitBaseTest):
    def test_create_item(self):
        item = ItemModel('test_item', 2.15, 1)

        self.assertEqual(item.name, 'test_item',
                         "The name of the item after creation does not equal the constructor argument.")
        self.assertEqual(item.price, 2.15,
                         "The price of the item after creation does not equal the constructor argument.")
        self.assertEqual(item.store_id, 1)
        self.assertIsNone(item.store)

    def test_item_json(self):
        item = ItemModel('test_item', 2.15, 1)
        expected = {
            'name': 'test_item',
            'price': 2.15
        }

        self.assertEqual(
            item.json(),
            expected,
            "The JSON export of the item is incorrect. Received {}, expected {}.".format(item.json(), expected))

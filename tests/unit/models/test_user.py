from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):
    def test_user_creation(self):
        user = UserModel('test_user', 'password')

        self.assertEqual(user.username, 'test_user')
        self.assertEqual(user.password, 'password')


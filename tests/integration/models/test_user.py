from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel('test_user', 'password')

            self.assertIsNone(user.find_by_id(1))
            self.assertIsNone(user.find_by_username('test_user'))

            user.save_to_db()

            self.assertIsNotNone(user.find_by_id(1))
            self.assertIsNotNone(user.find_by_username('test_user'))

            user.delete_from_db()

            self.assertIsNone(user.find_by_id(1))
            self.assertIsNone(user.find_by_username('test_user'))

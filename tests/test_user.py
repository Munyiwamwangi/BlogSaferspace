import unittest
from app import User

class UserTest(unittest.TestCase):
    def setUp(self):
        self.new_user = User(password = 'password')

    def test_login_scope(self):
            with self.assertRaises(AttributeError):
                self.new_user.password

    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password('password'))
import unittest
from app import Post


class UserTest(unittest.TestCase):
    def setUp(self):
        self.new_post = Post(password = 'password')

    def test_login_scope(self):
            with self.assertRaises(AttributeError):
                self.new_post.password

    def test_password_verification(self):
        self.assertTrue(self.new_post.verify_password('password'))
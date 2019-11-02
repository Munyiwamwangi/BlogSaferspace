import unittest
from app import Comment
from flask import current_app
from app import create_app

#this is a basic test manager
class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('development')
        self.app_context = self.app.app_context()
        self.app_context.push()

# prevents default faults such as unintended addition of info into the db
    def tearDown(self):
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)
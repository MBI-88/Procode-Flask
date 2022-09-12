# Test basico de la aplicacion
# Packages
import unittest
from app import create_app,db
from flask import current_app

# Test Classes

class BasicsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_app_exists(self) -> None:
        self.assertFalse(current_app is None)
    
    def test_app_is_testing(self) -> None:
        self.assertTrue(current_app.config['TESTING'])
    
    
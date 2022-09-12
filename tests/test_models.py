# Test para probar los modelos
# Packages
import unittest,time
from app.models import User,Role
from datetime import datetime
from app import create_app,db

# Test Classes
class UserModelTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
    
    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_password_setter(self) -> None:
        usr = User(password='cat')
        self.assertTrue(usr.password_hash is not None)
    
    def test_no_password_getter(self) -> None:
        usr = User(password='cat')
        with self.assertRaises(AttributeError):
            usr.password
    
    def test_password_verification(self) -> None:
        user = User(password='cat')
        self.assertTrue(user.verify_password('cat'))
        self.assertFalse(user.verify_password('dog'))
    
    def test_salt_password(self) -> None:
        user_1 = User(password='cat')
        user_2 = User(password='dog')
        self.assertTrue(user_1.password_hash != user_2.password_hash)
    
    
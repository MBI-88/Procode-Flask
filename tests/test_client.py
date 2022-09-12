# Test del cliente de la aplicacion
# Packages
import unittest,re
from app import create_app,db
from app.models import User,Role


# Test Classes

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)
        
        # registrando al administrador
        root = User(username='Root',password='toor')
        db.session.add(root)
        db.session.commit()
    
    
    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    
    def test_home_page(self) -> None:
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
        self.assertTrue('Comentar' in response.get_data(as_text=True))
        
    
    def test_register_login(self) -> None:
        # registrar usuario
        response = self.client.post('/auth/register',
                                    data ={
                                        'name':'testCase',
                                        'password':'password',
                                        'password2':'password'
                                    })
        self.assertTrue(response.status_code == 302)
        
        # logiar ususrio
        response = self.client.post('/auth/login',
                                    data={
                                        'name':'testCase',
                                        'password':'password',
                                        'remember_me':True
                                    },follow_redirects=True)
        
        data = response.get_data(as_text=True)
        self.assertTrue(re.search('testCase',data))
        
        # log out
        response = self.client.get('/auth/logout')
        self.assertEqual(response.status_code,200)
        
    
    
    def test_Admin_login(self) -> None:
        response = self.client.post('/auth/login',
                                    data={
                                        'name':'Root',
                                        'password':'toor',
                                        'remember_me':True
                                    },follow_redirects=True)
        
        data = response.get_data(as_text=True)
        self.assertTrue(re.search('Root',data))
        
        
        
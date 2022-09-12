# Test para la api
# Packages
import unittest
from app import db,create_app
import json
from base64 import b64encode
from app.models import Role,User


# Test Classes
class APITestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client()
        
        # insertando al administrador
        root = User(username='Root',password='toor')
        db.session.add(root)
        db.session.commit()
    
    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def get_api_headers(self,username:str,password:str,post=False) -> dict:
        
        content_type = 'multipart/form-data' if post else 'application/json'
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': content_type 
        }
    
    def test_404(self) -> None:
        response = self.client.get('/wrong/url',headers = self.get_api_headers('nadie','nada'))
        self.assertEqual(response.status_code,404)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['error'],'not found') 
    
    
    def test_no_auth(self) -> None:
        response = self.client.get('/api/v1/posts/2',content_type='application/json')
        self.assertEqual(response.status_code,401)
    
    
    def test_bad_auth(self) -> None:
        response = self.client.get('/api/v1/register/',
                                   headers=self.get_api_headers('Root','password'))
        self.assertEqual(response.status_code,401)
    
    
    def test_good_auth(self) -> None:
        response = self.client.get('/api/v1/users/',
                                   headers=self.get_api_headers('Root','toor'))
        self.assertEqual(response.status_code,200)
    
    
    def test_bad_token(self) -> None:
        response = self.client.get('/api/v1/users/',
                                   headers=self.get_api_headers('ningun_Token',''))
        self.assertEqual(response.status_code,401)
    
    def test_get_token_and_content(self) -> None:
        response = self.client.get('/api/v1/token/',
                                   headers=self.get_api_headers('Root','toor'))
        
        self.assertEqual(response.status_code,200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(json_response.get('token'))
        token = json_response.get('token')
        
        # peticion con token 
        response = self.client.get('/api/v1/users/',
                                   headers=self.get_api_headers(token,''))
        self.assertEqual(response.status_code,200)
    
    
    def test_security_api(self ) -> None:
        response = self.client.get('/api/v1/users/',
                                   headers=self.get_api_headers('',''))
        self.assertEqual(response.status_code,401)
    
    
    def test_register_user(self) -> None:
        response = self.client.get('/api/v1/register/',
                                   headers=self.get_api_headers('Root','toor'))
        self.assertEqual(response.status_code,200)
        
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(json_response.get('csrf_token'))
        csrf_token = json_response.get('csrf_token')
        
        # haciendo el post 
        response = self.client.post('/api/v1/register/',
                                    headers=self.get_api_headers('Root','toor',True),
                                    data={
                                        'csrf_token':csrf_token,
                                        'name':'John',
                                        'password':'password',
                                        'password2':'password'
                                    })
        
        self.assertEqual(response.status_code,200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(json_response.get('done'))
        
        
        
        
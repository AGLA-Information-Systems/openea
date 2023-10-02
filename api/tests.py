import base64
from django.test import TestCase
from rest_framework.test import APIClient
from utils.test.helpers import populate_test_env

class APITestCase(TestCase):
    client = APIClient()

    def setUp(self):
        populate_test_env(self)

    def test_basic_authentication(self):
        creds = base64.b64encode('org_1_user_1:12345'.encode()).decode()
        
        response = self.client.get('/api/rest/concepts/', HTTP_AUTHORIZATION = 'Basic '+ creds, format='json')
        self.assertEqual(response.status_code, 200, response.content)

    def test_session_authentication(self):
        logged_in = self.client.login(username='org_1_user_1', password='12345')
        self.assertTrue(logged_in)
        response = self.client.get('/api/rest/concepts/', format='json')
        self.assertEqual(response.status_code, 200, response.content)

    def test_get_token(self):
        response = self.client.post('/api/token/', {'username': 'org_1_user_1', 'password': '12345'}, format='json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        token = data.get('token')
        self.assertTrue(token)

        headers = {
            'AUTHORIZATION': 'Bearer ' + token,
        }
        response = self.client.get('/api/rest/concepts/', headers=headers, format='json')
        self.assertEqual(response.status_code, 200, response.content)

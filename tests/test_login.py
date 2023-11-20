import requests
import unittest
from db import referee_id_connection
from decouple import config

TEST_URL = config("TEST_URL", default="https://referite-6538ffaf77b0.herokuapp.com/")
AUDIENCE_TOKEN = config("AUDIENCE_TOKEN")

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.url = TEST_URL
        self.audienceToken = AUDIENCE_TOKEN

    def get_handler(self, url, token):
        return requests.get(
            f'{self.url}{url}',
            headers={
                'authorization': token
            }
        )

    def post_handler(self, url, data):
        return requests.post(
            f'{self.url}{url}',
            data=data,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )

    def test_login_valid_username_password(self):
        """Test login with valid username and password"""
        data = {'username': 'referee', 'password': 'referee123'}
        r = self.post_handler('api/auth/token', data)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()['expired'], referee_id_connection.find_one({'username': data['username']})['expired'])

    def test_login_valid_username_invalid_password(self):
        """Test login with valid username and invalid password"""
        data = {'username': 'referee', 'password': 'referee'}
        r = self.post_handler('api/auth/token', data)
        self.assertEqual(r.status_code, 401)
        self.assertEqual(r.text, '{"detail":"Please, Login"}')

    def test_login_invalid_username_valid_password(self):
        """Test login with invalid username and valid password"""
        data = {'username': 'tester', 'password': 'referee123'}
        r = self.post_handler('api/auth/token', data)
        self.assertEqual(r.status_code, 401)
        self.assertEqual(r.text, '{"detail":"Please, Login"}')

    def test_login_invalid_username_invalid_password(self):
        """Test login with invalid username and invalid password"""
        data = {'username': 'tester', 'password': 'referee'}
        r = self.post_handler('api/auth/token', data)
        self.assertEqual(r.status_code, 401)
        self.assertEqual(r.text, '{"detail":"Please, Login"}')

    @unittest.skip("Skip")
    def test_login_empty_username_empty_password(self):
        """Test login with empty username and empty password"""
        data = {'username': '', 'password': ''}
        r = self.post_handler('api/auth/token', data)
        self.assertEqual(r.status_code, 401)
        self.assertEqual(r.text, '{"detail":"Please, Login"}')

    def test_login_special_symbol(self):
        """Test login with special symbol"""
        data = {'username': 'referee', 'password': 'referee!@#$%^&*()'}
        r = self.post_handler('api/auth/token', data)
        self.assertEqual(r.status_code, 401)
        self.assertEqual(r.text, '{"detail":"Please, Login"}')

    def test_login_and_check_permission(self):
        """Test login with valid username and password then check permission"""
        data = {'username': 'referee', 'password': 'referee123'}
        r = self.post_handler('api/auth/token', data)
        r1 = self.get_handler('api/schedule/all', r.json()['access_token'])
        self.assertEqual(r1.status_code, 200)

    def test_permission(self):
        """Test permission for wrong authorization and audience authorization"""
        lst_url = ["api/schedule/all", "api/schedule/sport"]
        for url in lst_url:
            r = self.get_handler(url, 'Toast')
            self.assertEqual(r.status_code, 401)
            self.assertEqual(r.text, '{"detail":"Please, Login"}')
            r1 = self.get_handler(url, self.audienceToken)
            self.assertEqual(r1.status_code, 200)

    def test_audience_permission(self):
        """Test permission for other page that audience cannot access"""
        # GET
        r = self.get_handler('api/record/detail/2024-08-01T00:00:00/1', self.audienceToken)
        self.assertEqual(r.status_code, 401)
        self.assertEqual(r.text, '{"detail":"Please, Login"}')
        # POST
        lst_url = ["api/record/verify", "api/record/medal/update"]
        for url in lst_url:
            r = requests.post(
                f'{self.url}{url}',
                headers={
                    'authorization': self.audienceToken
                }
            )
            self.assertEqual(r.status_code, 401)
            self.assertEqual(r.text, '{"detail":"Please, Login"}')


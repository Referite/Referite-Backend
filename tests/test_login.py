import requests
import unittest

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.url = 'https://referite-6538ffaf77b0.herokuapp.com/'

    def test_login_valid_username_password(self):
        """Test login with valid username and password"""
        data = {'username': 'referee', 'password': 'referee123'}
        r = requests.post(
            f'{self.url}api/auth/token',
            data=data,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        self.assertEqual(r.status_code, 201)

    def test_login_valid_username_invalid_password(self):
        """Test login with valid username and invalid password"""
        data = {'username': 'referee', 'password': 'referee'}
        r = requests.post(
            f'{self.url}api/auth/token',
            data=data,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        self.assertEqual(r.status_code, 401)

    def test_login_invalid_username_valid_password(self):
        """Test login with invalid username and valid password"""
        data = {'username': 'tester', 'password': 'referee123'}
        r = requests.post(
            f'{self.url}api/auth/token',
            data=data,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        self.assertEqual(r.status_code, 401)

    def test_login_invalid_username_invalid_password(self):
        """Test login with invalid username and invalid password"""
        data = {'username': 'tester', 'password': 'referee'}
        r = requests.post(
            f'{self.url}api/auth/token',
            data=data,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        self.assertEqual(r.status_code, 401)

    def test_login_empty_username_empty_password(self):
        """Test login with empty username and empty password"""
        data = {'username': '', 'password': ''}
        r = requests.post(
            f'{self.url}api/auth/token',
            data=data,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        self.assertEqual(r.status_code, 401)

    def test_login_special_symbol(self):
        """Test login with special symbol"""
        data = {'username': 'referee', 'password': 'referee!@#$%^&*()'}
        r = requests.post(
            f'{self.url}api/auth/token',
            data=data,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        self.assertEqual(r.status_code, 401)
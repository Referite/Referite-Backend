import requests
import unittest

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.url = 'https://referite-6538ffaf77b0.herokuapp.com/'
        self.audienceToken = '02e2cdc6ac5d17a2bb67824c91f51ac55ce46465133f92233e3daa552120bcb3'

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

    def test_login_and_check_permission(self):
        """Test login with valid username and password then check permission"""
        data = {'username': 'referee', 'password': 'referee123'}
        r = requests.post(
            f'{self.url}api/auth/token',
            data=data,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        token = r.json()['access_token']
        r = requests.get(
            f'{self.url}api/schedule/all',
            headers={
                'authorization': token
            }
        )
        self.assertEqual(r.status_code, 200)

    def test_permission(self):
        """Test permission for wrong authorization and audience authorization"""
        lst_url = ["api/schedule/all", "api/schedule/sport"]
        for url in lst_url:
            r = requests.get(
                f'{self.url}{url}',
                headers={
                    'authorization': 'Toast'
                }
            )
            self.assertEqual(r.status_code, 401)
            r1 = requests.get(
                f'{self.url}{url}',
                headers={
                    'authorization': self.audienceToken
                }
            )
            self.assertEqual(r1.status_code, 200)

    def test_audience_permission(self):
        """Test permission for other page that audience cannot access"""
        # GET
        r = requests.get(
            f'{self.url}{"api/record/detail/2024-08-01T00:00:00/1"}',
            headers={
                'authorization': self.audienceToken
            }
        )
        self.assertEqual(r.status_code, 401)
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


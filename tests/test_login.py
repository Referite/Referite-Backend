import requests
import unittest

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.url = 'https://referite-6538ffaf77b0.herokuapp.com/'

    def test_login(self):
        data = {'username': 'referee', 'password': 'referee123'}
        r = requests.post(
            f'{self.url}api/auth/token',
            data=data,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        self.assertEqual(r.status_code, 201)
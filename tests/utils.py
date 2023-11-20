import requests
from decouple import config

TEST_URL = config("TEST_URL", default="https://referite-6538ffaf77b0.herokuapp.com/")

def get_handler(url, token):
    """GET url with authorization token"""
    return requests.get(
        f'{TEST_URL}{url}',
        headers={
            'authorization': token
        }
    )

def login_post_handler(url, data):
    """POST form data to url without authorization token"""
    return requests.post(
        f'{TEST_URL}{url}',
        data=data,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    )

def data_post_handler(url, token, data=None):
    """POST data to url with authorization token"""
    if data is None:
        data = {}
    return requests.post(
        f'{TEST_URL}{url}',
        data=data,
        headers={
            'Content-Type': 'application/json',
            'authorization': token
        }
    )
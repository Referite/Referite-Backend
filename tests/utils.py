from main import app
from fastapi.testclient import TestClient
from urllib.parse import urlencode

client = TestClient(app)


def get_handler(path, token):
    """GET url with authorization token"""
    return client.get(path,
        headers={
            'authorization': token
        }
    )

def login_post_handler(path, data):
    """POST form data to url without authorization token"""
    return client.post(path,
        data=urlencode(data),
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    )

def data_post_handler(path, token, data=None):
    """POST data to url with authorization token"""
    if data is None:
        data = {}
    return client.post(
        path,
        json=data,
        headers={
            'Content-Type': 'application/json',
            'authorization': token
        }
    )

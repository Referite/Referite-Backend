from main import app
from fastapi.testclient import TestClient
from urllib.parse import urlencode
from selenium.webdriver.common.by import By
from db import sport_schedule_connection

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

def browser_login(browser, username, password):
    """Login to browser with username and password"""
    browser.get("http://localhost:5173/")
    browser.implicitly_wait(3)
    browser.find_element(By.XPATH, '//*[@id="root"]/div/div/input[1]').send_keys(username) # username
    browser.find_element(By.XPATH, '//*[@id="root"]/div/div/input[2]').send_keys(password) # password
    browser.find_element(By.XPATH, '//*[@id="root"]/div/div/button').click() # Sign in button
    browser.implicitly_wait(30)

def change_status_to_trophy():
    """Change status of sport type to TROPHY"""
    query = {"sport.sport_id": 4, "sport.sport_type.type_id": 39, "sport.sport_type.status": "RECORDED"}
    update = {"$set": {"sport.$.sport_type.$[typeElem].status": "TROPHY"}}
    sport_schedule_connection.update_one(query, update, array_filters=[{"typeElem.type_id": 39, "typeElem.status": "RECORDED"}])
    print("updated")
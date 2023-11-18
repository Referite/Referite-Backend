import pytest
from fastapi.testclient import TestClient
from main import app
from db import sport_schedule_connection

@pytest.fixture(scope="module")
def test_db():
    # Set up the test database
    sport_schedule_connection.insert_one(
        {
            "datetime": "2021-08-01T00:00:00",
            "sport": [
                {
                    "sport_id": 1,
                    "sport_name": "Football",
                    "is_ceremonies": False,
                    "sport_type": [
                        {
                            "type_id": 1,
                            "type_name": "11v11",
                            "status": "recorded",
                        },
                        {"type_id": 2, "type_name": "7v7", "status": "trophy"},
                    ],
                }
            ],
        }
    )

    # Pass the DB connection to the test
    yield sport_schedule_connection

    # Delete the test database
    sport_schedule_connection.drop()


# Use a fixture to create an instance of the FastAPI app
@pytest.fixture(scope="module")
def test_app():
    return app

def test_read_main(test_app, test_db):
    with TestClient(test_app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello from Refrite✌️"}

def test_read_api(test_app, test_db):
    with TestClient(test_app) as client:
        response = client.get("/api")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello from Refrite✌️"}

def test_add_some_data(test_app, test_db):
    with TestClient(test_app) as client:
        response = client.get("/mock")
        assert response.status_code == 200
        assert response.json() == {"message": "data mocked"}

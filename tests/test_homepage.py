import unittest
from unittest.mock import patch
from db import sport_schedule_connection
from tests.utils import get_handler, login_post_handler, data_post_handler
from utils import calculate_sport_status
from router.schedule import get_schedule

class TestHomepage(unittest.TestCase):
    def test_get_all_sport_without_token(self):
        """Test get all sport without token"""
        r = get_handler('api/schedule/all', "")
        self.assertEqual(r.status_code, 401)

    def schedule(self):
        current_schedule = list(sport_schedule_connection.find({}, {"_id": 0}))
        for schedule in current_schedule:
            for sport in schedule["sport"]:
                sport["sport_status"] = calculate_sport_status(sport["sport_type"])
        return {"schedule_list": current_schedule}
    def test_get_all_sport_with_token(self):
        """Test get all sport with token"""
        data = {'username': 'referee', 'password': 'referee123'}
        r = login_post_handler('api/auth/token', data)
        r1 = get_handler('api/schedule/all', r.json()['access_token'])
        self.assertEqual(r1.json()["schedule_list"], self.schedule()['schedule_list'])
        self.assertEqual(r1.status_code, 200)

    def test_get_all_schedule_without_token(self):
        """Test get all schedule without token"""
        r = get_handler('api/schedule/sport', "")
        self.assertEqual(r.status_code, 401)

    def test_get_all_schedule_with_token(self):
        """Test get all schedule with token"""
        data = {'username': 'referee', 'password': 'referee123'}
        r = login_post_handler('api/auth/token', data)
        r1 = get_handler('api/schedule/sport', r.json()['access_token'])
        self.assertEqual(r1.status_code, 200)

    def test_add_schedule_without_token(self):
        """Test add schedule without token"""
        r = data_post_handler('api/schedule/add', "")
        self.assertEqual(r.status_code, 401)
